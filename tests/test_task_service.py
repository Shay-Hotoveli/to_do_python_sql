import uuid
from app.services import task_service
from app.services import user_service

def test_create_and_get_task(db, clean_user_db):
    username = f"taskuser_{uuid.uuid4().hex[:6]}"
    email = f"{username}@test.com"
    password = "testpass"
    gender = "other"
    user_service.create_user(username, password, email, gender)
    user = user_service.get_user_by_username(username)
    user_id = user["user_id"]
    header = "Test Task"
    description = "Test Description"
    task_service.create_task(header, description, user_id)
    tasks = task_service.get_tasks_by_user(user_id)
    assert len(tasks) == 1
    assert tasks[0]["task_header"] == header
    assert tasks[0]["task_description"] == description
    assert tasks[0]["user_id"] == user_id

def test_get_task_by_id(db, clean_user_db):
    username = f"gettask_{uuid.uuid4().hex[:6]}"
    email = f"{username}@mail.com"
    password = "pass123"
    gender = "female"
    user_service.create_user(username, password, email, gender)
    user = user_service.get_user_by_username(username)
    user_id = user["user_id"]
    task_service.create_task("Header1", "Desc1", user_id)
    task = task_service.get_tasks_by_user(user_id)[0]
    task_id = task["task_id"]
    fetched = task_service.get_task_by_id(task_id, user_id)
    assert fetched is not None
    assert fetched["task_id"] == task_id
    assert fetched["task_header"] == "Header1"

def test_update_task(db, clean_user_db):
    username = f"updatetask_{uuid.uuid4().hex[:6]}"
    email = f"{username}@mail.com"
    password = "pass"
    gender = "male"
    user_service.create_user(username, password, email, gender)
    user = user_service.get_user_by_username(username)
    user_id = user["user_id"]
    task_service.create_task("Old Header", "Old Desc", user_id)
    task = task_service.get_tasks_by_user(user_id)[0]
    task_id = task["task_id"]
    task_service.update_task(task_id, user_id, "New Header", "New Desc", is_complete=True)
    updated = task_service.get_task_by_id(task_id, user_id)
    assert updated["task_header"] == "New Header"
    assert updated["task_description"] == "New Desc"
    assert updated["complete"] == 1
    assert updated["finish_time"] is not None

def test_delete_task(db, clean_user_db):
    username = f"deltask_{uuid.uuid4().hex[:6]}"
    email = f"{username}@mail.com"
    password = "pass"
    gender = "male"
    user_service.create_user(username, password, email, gender)
    user = user_service.get_user_by_username(username)
    user_id = user["user_id"]
    task_service.create_task("To Delete", "Should be deleted", user_id)
    task = task_service.get_tasks_by_user(user_id)[0]
    task_id = task["task_id"]
    task_service.delete_task_by_id(task_id, user_id)
    deleted = task_service.get_task_by_id(task_id, user_id)
    assert deleted is None
