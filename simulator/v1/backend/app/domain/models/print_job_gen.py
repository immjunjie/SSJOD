import random
from datetime import datetime, timedelta
from typing import Dict, Any, List
import uuid
from enum import Enum


class PrintState(Enum):
    PRE_PRINT = "pre_print"
    PRINTING = "printing"
    PAUSED = "paused"
    POST_PRINT = "post_print"
    WAIT_CLEANUP = "wait_cleanup"
    ERROR = "error"


class PrintJobDataGenerator:
    def __init__(self):
        self._current_job = None
        self._job_start_time = None
        self._estimated_duration = None
        self.refresh_job()

    # ===== 核心控制方法 =====
    def refresh_job(self):
        """初始化或重置打印任务"""
        self._job_start_time = datetime.now()
        self._estimated_duration = timedelta(minutes=random.randint(30, 300))  # 30-300分钟
        self._current_job = self._generate_base_structure()

    def update_progress(self):
        """基于实时更新进度（应在外部定期调用）"""
        if self._current_job["state"] == PrintState.PRINTING.value:
            elapsed = datetime.now() - self._job_start_time
            progress = min(0.99, elapsed / self._estimated_duration)
            self._current_job["progress"] = round(progress, 2)
            self._current_job["time_elapsed"] = int(elapsed.total_seconds())

    # ===== 分层生成组件 =====
    def _generate_base_structure(self) -> Dict[str, Any]:
        """生成任务基础结构"""
        job_id = str(uuid.uuid4())

        metadata = self._generate_metadata(job_id)
        time_info = self._generate_time_info()
        progress_info = self._generate_progress_info()
        source_info = self._generate_source_info()
        gcode_info = self._generate_gcode_info(job_id)
        state_info = self._generate_state_info()

        base = {
            "metadata": metadata,
            "time_info": time_info,
            "progress_info": progress_info,
            "source_info": source_info,
            "gcode_info": gcode_info,
            "state_info": state_info
        }

        # 平铺结构用于兼容旧版
        return {**base, **metadata, **time_info, **progress_info}

    def _generate_metadata(self, job_id: str) -> Dict[str, Any]:
        # 生成元数据组建
        return {
            "uuid": job_id,
            "name": self._generate_job_name(),
            "reprint_original_uuid": "" if random.random() > 0.1 else str(uuid.uuid4())
        }

    def _generate_time_info(self) -> Dict[str, Any]:
        """生成时间相关组件"""
        return {
            "datetime_started": self._job_start_time.isoformat(),
            "datetime_finished": "",
            "datetime_cleaned": "",
            "time_total": int(self._estimated_duration.total_seconds()),
            "time_elapsed": 0
        }

    def _generate_progress_info(self) -> Dict[str, Any]:
        """生成进度组件"""
        return {
            "progress": 0.0,
            "current_layer": 0,
            "total_layers": random.randint(50, 500)
        }

    def _generate_source_info(self) -> Dict[str, Any]:
        """生成来源组件"""
        return {
            "source": random.choices(
                ["WEB_API", "USB", "CLOUD"],
                weights=[0.7, 0.2, 0.1]
            )[0],
            "source_application": "Ultimaker Cura",
            "source_user": "" if random.random() > 0.8 else f"user_{random.randint(1, 100)}"
        }

    # 修改 gcode_info，使用传入的 uuid
    def _generate_gcode_info(self, job_id: str) -> Dict[str, Any]:
        # 生成GCODE相关数据
        return {
            "gcode": f"job_{job_id[:8]}.gcode",
            "container": f"container_{job_id[:8]}",
            "pause_source": ""
        }

    def _generate_state_info(self) -> Dict[str, Any]:
        """生成状态组件"""
        return {
            "state": PrintState.PRE_PRINT.value,
            "result": "",
            "error_info": {} if random.random() > 0.9 else {"code": random.randint(1, 10)}
        }

    # ===== 业务逻辑方法 =====
    def _generate_job_name(self) -> str:
        """智能生成任务名称"""
        prefixes = ["UM3", "UMS5", "Custom"]
        models = ["3DBenchy", "Calibration", "Functional_Part"]
        return f"{random.choice(prefixes)}_{random.choice(models)}_v{random.randint(1, 10)}"

    def start_printing(self):
        """开始打印业务逻辑"""
        self._current_job["state"] = PrintState.PRINTING.value
        self._job_start_time = datetime.now()

    def finish_printing(self, success: bool = True):
        """完成打印业务逻辑"""
        finish_time = datetime.now()
        self._current_job.update({
            "state": PrintState.POST_PRINT.value if success else PrintState.ERROR.value,
            "result": "Finished" if success else random.choice(["Failed", "Aborted"]),
            "datetime_finished": finish_time.isoformat(),
            "progress": 1.0,
            "time_elapsed": int((finish_time - self._job_start_time).total_seconds())
        })

    # ===== 访问接口 =====
    @property
    def current_job(self) -> Dict[str, Any]:
        """获取当前完整任务数据"""
        return self._current_job

    def get_component(self, component: str) -> Dict[str, Any]:
        """按组件获取数据"""
        if component in ["metadata", "time_info", "progress_info",
                         "source_info", "gcode_info", "state_info"]:
            return self._current_job[component]
        raise ValueError(f"Invalid component: {component}")

    def get_field(self, field: str) -> Any:
        """获取特定字段值（兼容旧版）"""
        return self._current_job.get(field)