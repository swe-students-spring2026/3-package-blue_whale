import pytest
from ghosty import ghosty

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
        for _ in range(6):
            ghosty.nudge("Do everything")

        assert ghosty._task_board["Do everything"]["progress"] == 100

    def test_nudge_missing_task(self):
        with pytest.raises(KeyError):
            ghosty.nudge("nonexistent task")

    def test_nudge_invalid_task_name(self):
        with pytest.raises(ValueError):
            ghosty.nudge("")
    


