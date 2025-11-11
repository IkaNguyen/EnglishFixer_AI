from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from collections import Counter # Thư viện tiện lợi để đếm

from ....db import session # Giả sử bạn có hàm get_db
from ....db import models # Giả sử bạn có model Submission và User
from ....core import security # Giả sử bạn có hàm get_current_user
from ....schemas.dashboard import UserDashboardStats, ErrorStat

router = APIRouter()

@router.get("/me/dashboard-stats", response_model=UserDashboardStats)
def get_user_dashboard_stats(
    db: Session = Depends(session.get_db), 
    current_user: models.User = Depends(security.get_current_user)
):
    """
    Tính toán và trả về dữ liệu thống kê cho người dùng đang đăng nhập.
    """
    # 1. Lấy tất cả bài nộp của người dùng
    submissions = db.query(models.Submission).filter(
        models.Submission.owner_id == current_user.id,
        models.Submission.result_json.isnot(None) # Chỉ lấy bài đã có kết quả
    ).all()

    if not submissions:
        return UserDashboardStats(total_submissions=0, common_errors=[])

    # 2. Đếm các loại lỗi từ 'result_json'
    error_counter = Counter()
    for sub in submissions:
        # Giả định result_json được lưu trong CSDL có cấu trúc này
        if 'feedback_details' in sub.result_json:
            for error in sub.result_json['feedback_details']:
                error_type = error.get('error_type', 'Other')
                error_counter[error_type] += 1
    
    # 3. Định dạng top 5 lỗi phổ biến
    common_errors = [
        ErrorStat(error_type=etype, count=count)
        for etype, count in error_counter.most_common(5)
    ]

    return UserDashboardStats(
        total_submissions=len(submissions),
        common_errors=common_errors
    )