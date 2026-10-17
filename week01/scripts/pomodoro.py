import argparse
import time
def run_timer(minutes:float,task:str)->None:
    total_seconds=int(minutes*60)
    print(f"开始专注：【{task}】共{minutes}分钟")
    for remaining in range(total_seconds,0,-1):
        mins,secs=divmod(remaining,60)
        print(f"\r 剩余时间：{mins:02d}:{secs:02d}",end="",flush=True)
        time.sleep(1)
    print(f"\n时间到！【{task}】完成，起来喝口咖啡！")
if __name__=="__main__":
    parser=argparse.ArgumentParser(description="命令行番茄钟")
    parser.add_argument("-m","--minutes",type=float,default=25,help="专注分钟数")
    parser.add_argument("-t","--task",default="写量化代码",help="当前任务名称")
    args=parser.parse_args()
    run_timer(args.minutes,args.task)
