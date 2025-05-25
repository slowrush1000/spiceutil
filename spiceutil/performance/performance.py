import datetime
import psutil
import os
import resource
import sys
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import version


class Performance:
    def __init__(self, t_log=None):
        self.__log = t_log
        #
        self.__wall_time = time.perf_counter()
        self.__start_wall_time = time.perf_counter()
        self.__end_wall_time = time.perf_counter()
        #
        self.__user_cpu_time = 0
        self.__system_cpu_time = 0
        self.__total_cpu_time = 0
        #
        self.__peak_memory_mb = 0
        #
        self.__process = psutil.Process(os.getpid())
        self.__mem_info_before = self.__process.memory_info()
        self.__initial_rss_mb = self.__mem_info_before.rss / (1024 * 1024)
        self.__current_rss_mb = self.__process.memory_info().rss / (1024 * 1024)

    def set_log(self, t_log):
        self.__log = t_log

    def end(self):
        try:
            self.__end_wall_time = time.perf_counter()
            self.__wall_time = self.__end_wall_time - self.__start_wall_time
            #
            rusage_info = resource.getrusage(resource.RUSAGE_SELF)
            #
            self.__user_cpu_time = rusage_info.ru_utime
            self.__system_cpu_time = rusage_info.ru_stime
            self.__total_cpu_time = self.__user_cpu_time + self.__system_cpu_time
            #
            self.__peak_memory_mb = rusage_info.ru_maxrss
            if os.uname().sysname == "Darwin":  # MacOS
                self.__peak_memory_mb = self.__peak_memory_mb / (1024 * 1024)
            else:  # Linux
                self.__peak_memory_mb = self.__peak_memory_mb / 1024
            #
            self.__current_rss_mb = self.__process.memory_info().rss / (1024 * 1024)
        except ImportError:
            s1 = "# error: resource module isnot supported in this system(ex: Windows), so performance isnot working!"
            if None != self.__log:
                self.__log.get_logger().error("# error: {s1}")
                self.__log.get_logger().info(
                    f"# spiceutil({version.Version().get_program_version()}) end ... {datetime.datetime.now()}\n"
                )
            else:
                print(f"# error: {s1}")
                print(
                    f"spiceutil({version.Version().get_program_version()}) end ... {datetime.datetime.now()}\n"
                )
            exit()
        except Exception as e:
            print(f"성능 측정 중 오류 발생: {e}")

    def get_wall_time_sec(self):
        return self.__wall_time

    def get_user_cpu_time_sec(self):
        return self.__user_cpu_time

    def get_system_cpu_time_sec(self):
        return self.__system_cpu_time

    def get_total_cpu_time_sec(self):
        return self.__total_cpu_time

    def get_cur_memory_mb(self):
        return self.__process.memory_info().rss / (1024 * 1024)

    def get_peak_memory_mb(self):
        return self.__peak_memory_mb

    def get_str(self):
        self.end()
        s1 = f"walltime(sec): {self.get_wall_time_sec():.1f} / "
        s1 += f"cpu(sec) {self.get_total_cpu_time_sec():.1f} "
        s1 += f"user {self.get_user_cpu_time_sec():.1f} "
        s1 += f"sys {self.get_system_cpu_time_sec():.1f} \n"
        s1 += f"# memory usage(mb) : cur_rss) {self.get_cur_memory_mb():.1f} / "
        s1 += f"peak_rss) {self.get_peak_memory_mb():.1f}"
        return s1

    def get_process_id(self):
        return self.__process
