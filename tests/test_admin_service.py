from app.services import admin_service, user_service
import uuid

def test_get_dashboard_counts(db):
    counts = admin_service.get_dashboard_counts()
    assert "task_count" in counts
    assert "user_count" in counts
    assert isinstance(counts["task_count"], int)
    assert isinstance(counts["user_count"], int)

def test_fetch_all_users(db):
    users = admin_service.fetch_all_users()
    assert isinstance(users, list)
    if users:
        user = users[0]
        assert "user_id" in user
        assert "user_name" in user
        assert "email" in user

def test_fetch_user_overview(db):
    overview = admin_service.fetch_user_overview()
    assert isinstance(overview, list)
    if overview:
        user = overview[0]
        assert "user_id" in user
        assert "total_tasks" in user
        assert "completed_tasks" in user
        assert "pending_tasks" in user
        assert "last_activity" in user

def test_delete_user_by_id(db, clean_user_db):
    username = f"tempuser_{uuid.uuid4().hex[:6]}"
    email = f"{username}@test.com"
    password = "test"
    gender = "male"
    user_service.create_user(username, password, email, gender)
    user = user_service.get_user_by_username(username)
    assert user is not None
    user_id = user["user_id"]
    admin_service.delete_user_by_id(user_id)
    deleted = user_service.get_user_by_username(username)
    assert deleted is None
