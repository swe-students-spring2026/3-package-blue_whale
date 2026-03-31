import pytest
from ghosty import ghosty
from unittest.mock import patch

class TestAssign:
    def setup_method(self):
        ghosty._task_board.clear()
    def test_assign_valid_task(self):
        result = ghosty.assign("Fix login bug", 3)
        assert isinstance(result, str)
        assert len(result) > 0
        assert "Fix login bug" in result

    def test_assign_stores_task(self):
        ghosty.assign("fix login bug", 2, category="high")
        assert "fix login bug" in ghosty._task_board
        assert ghosty._task_board["fix login bug"]["hours"] == 2


    def test_assign_progress_starts_at_zero(self):
        ghosty.assign("New feature", 5, category="low")
        assert ghosty._task_board["New feature"]["progress"] == 0

    def test_assign_invalid_hours(self):
        with pytest.raises(ValueError):
            ghosty.assign("Bad task", -1)
    def test_assign_invalid_task_name(self):
        with pytest.raises(ValueError):
            ghosty.assign("", 3)

    def test_assign_invalid_category(self):
        with pytest.raises(ValueError):
            ghosty.assign("fix login bug", 2, category="urgent")

class TestCheckIn:
    def setup_method(self):
        ghosty._task_board.clear()

    def test_checkin_empty_board(self):
        result = ghosty.check_in()
        assert isinstance(result, str)
        assert "No tasks" in result

    def test_checkin_all_tasks(self):
        ghosty.assign("Task A", 4)
        ghosty.assign("Task B", 2, category="high")
        result = ghosty.check_in()
        assert "Task A" in result
        assert "Task B" in result

    def test_checkin_specific_task(self):
        ghosty.assign("Fix bug", 3, category="critical")
        result = ghosty.check_in("Fix bug")
        assert "Fix bug" in result
        assert "3" in result

    def test_checkin_task_not_found(self):
        with pytest.raises(KeyError):
            ghosty.check_in("nonexistent task")

    def test_checkin_shows_zero_progress(self):
        ghosty.assign("Do work", 10)
        result = ghosty.check_in("Do work")
        assert "0%" in result

    def test_checkin_hides_completed_tasks_by_default(self):
        ghosty.assign("Done task", 1)
        while ghosty._task_board["Done task"]["progress"] < 100:
            ghosty.nudge("Done task")

        result = ghosty.check_in()
        assert "No active tasks" in result

    def test_checkin_can_include_completed_tasks(self):
        ghosty.assign("Done task", 1)
        while ghosty._task_board["Done task"]["progress"] < 100:
            ghosty.nudge("Done task")

        result = ghosty.check_in(include_completed=True)
        assert "Done task" in result

class TestExcuse:
    def test_excuse_high_seriousness(self):
        result= ghosty.excuse("my laptop ran away", "high")

        assert isinstance(result, str)
        assert "my laptop ran away" in result
        assert "critical" in result
    def test_excuse_medium_seriousness(self):
        result = ghosty.excuse("wifi stopped believing in me", "medium")

        assert isinstance(result, str)
        assert "wifi stopped believing in me" in result
        assert "emotionally" in result
    
    def test_excuse_low_seriousness(self):
        result = ghosty.excuse("too comfy", "low")
        
        assert isinstance(result, str)
        assert "too comfy" in result
        assert "nothing" in result
    
    def test_excuse_default_seriousness(self):
        result = ghosty.excuse("got lost vibing")
        
        assert isinstance(result, str)
        assert "got lost vibing" in result
        assert "emotionally" in result
    
    def test_excuse_invalid_reason(self):
        with pytest.raises(ValueError):
            ghosty.excuse("", "high")
    
    def test_excuse_invalid_seriousness(self):
        with pytest.raises(ValueError):
            ghosty.excuse("sick", "urgent")


class TestGreet:
    def test_greet_without_arguments_returns_known_random_message(self):
        result = ghosty.greet()
        options = [
            "Hey! Just catching up on the thread now. What did I miss?",
            "Morning! How is your part coming along? Looking great so far!",
            "Just grabbing coffee and then diving deep into my task. Update soon.",
            "Love the direction this is going. Keep it up, team!",
        ]
        assert result in options

    def test_greet_returns_non_empty_string(self):
        result = ghosty.greet()
        assert isinstance(result, str)
        assert len(result) > 0

    def test_greet_supports_catch_up_intent(self):
        result = ghosty.greet(presence="reappearing", intent="catch_up")
        assert "Ghosty" in result
        assert "catching up" in result

    def test_greet_supports_ask_about_teammate_intent(self):
        result = ghosty.greet(presence="active", intent="ask_about_teammate", teammate="Celia's section")
        assert "Celia" in result

    def test_greet_supports_promise_progress_with_blocker(self):
        result = ghosty.greet(intent="promise_progress", blocker="login bugs")
        assert "login bugs" in result

    def test_greet_invalid_presence(self):
        with pytest.raises(ValueError):
            ghosty.greet(presence="invisible")

    def test_greet_invalid_intent(self):
        with pytest.raises(ValueError):
            ghosty.greet(intent="random_vibes")

    def test_greet_invalid_teammate(self):
        with pytest.raises(ValueError):
            ghosty.greet(intent="ask_about_teammate", teammate="")


class TestNudge:
    def setup_method(self):
        ghosty._task_board.clear()

    def test_nudge_updates_progress(self):
        ghosty.assign("Fix login bug", 3)
        result = ghosty.nudge("Fix login bug")

        assert isinstance(result, str)
        assert ghosty._task_board["Fix login bug"]["progress"] == 20
        assert ghosty._task_board["Fix login bug"]["nudged"] is True

    def test_nudge_caps_progress_at_hundred(self):
        ghosty.assign("Do everything", 5)
        while ghosty._task_board["Do everything"]["progress"] < 100:
            ghosty.nudge("Do everything")

        assert ghosty._task_board["Do everything"]["progress"] == 100

    def test_nudge_missing_task(self):
        with pytest.raises(KeyError):
            ghosty.nudge("nonexistent task")

    def test_nudge_invalid_task_name(self):
        with pytest.raises(KeyError):
            ghosty.nudge("")

    def test_nudge_invalid_scold_val(self):
        with pytest.raises(KeyError):
            ghosty.nudge("A task", scold = "Yesterday")
    
    def test_nudge_invalid_tired_val(self):
        with pytest.raises(KeyError):
            ghosty.nudge("Today's task", scold = True, tired="Maybe")

    def test_nudge_causing_angry_tired_and_scold(self):
        ghosty.assign("Hard task", 4)
        ghosty.nudge("Hard task", scold=True, tired=True)

        assert ghosty._task_board["Hard task"]["angry"] is True

    def test_nudge_causing_angry_overly_scolding(self):
        ghosty.assign("Hard task", 4)
        ghosty.nudge("Hard task", scold=True)
        ghosty.nudge("Hard task", scold=True)
        ghosty.nudge("Hard task", scold=True)

        assert ghosty._task_board["Hard task"]["angry"] is True
    
    def test_nudge_when_already_angry(self):
        ghosty.assign("Task", 4)
        for _ in range(3):
            ghosty.nudge("Task", scold=True)

        result = ghosty.nudge("Task")

        assert "still ANGRY" in result
    
    def test_angry_does_not_change_progress(self):
        ghosty.assign("Task", 4)

        for _ in range(3):
            ghosty.nudge("Task", scold=True)

        before = ghosty._task_board["Task"]["progress"]

        ghosty.nudge("Task")

        after = ghosty._task_board["Task"]["progress"]

        assert before == after
    
    def test_over_sixty_random_not_working(self):
        ghosty.assign("Task", 4)

        ghosty.nudge("Task", scold=True)
        ghosty.nudge("Task", scold=True)

        with patch("random.getrandbits", return_value=1):
            result = ghosty.nudge("Task", scold=False)

        assert "doesn't want to work" in result

    def test_over_sixty_and_scold(self):
        ghosty.assign("Hard task", 4)
        ghosty.nudge("Hard task")
        ghosty.nudge("Hard task")
        ghosty.nudge("Hard task")
        ghosty.nudge("Hard task", scold=True)

        assert ghosty._task_board["Hard task"]["progress"] == 90
    
    def test_tired(self):
        ghosty.assign("Hard task", 4)
        ghosty.nudge("Hard task", tired=True)

        assert ghosty._task_board["Hard task"]["progress"] == 10
    
    def test_scold(self):
        ghosty.assign("Hard task", 4)
        ghosty.nudge("Hard task", scold=True)

        assert ghosty._task_board["Hard task"]["progress"] == 30
    
    def test_random_no_progress_change(self):
        ghosty.assign("Task", 4)

        ghosty.nudge("Task", scold=True)
        ghosty.nudge("Task", scold=True)

        before = ghosty._task_board["Task"]["progress"]

        with patch("random.getrandbits", return_value=1):
            ghosty.nudge("Task", scold=False)

        after = ghosty._task_board["Task"]["progress"]

        assert before == after

class TestTaskHelpers:
    def setup_method(self):
        ghosty._task_board.clear()

    def test_remove_task_success(self):
        ghosty.assign("Temp task", 2)

        result = ghosty.remove_task("Temp task")

        assert "removed" in result
        assert "Temp task" not in ghosty._task_board

    def test_remove_task_missing(self):
        with pytest.raises(KeyError):
            ghosty.remove_task("missing")

    def test_remove_task_invalid_name(self):
        with pytest.raises(ValueError):
            ghosty.remove_task("")

    def test_clear_completed_removes_only_completed_tasks(self):
        ghosty.assign("Done task", 1)
        ghosty.assign("Active task", 2)

        while ghosty._task_board["Done task"]["progress"] < 100:
            ghosty.nudge("Done task")

        result = ghosty.clear_completed()

        assert "Cleared 1" in result
        assert "Done task" not in ghosty._task_board
        assert "Active task" in ghosty._task_board
    


