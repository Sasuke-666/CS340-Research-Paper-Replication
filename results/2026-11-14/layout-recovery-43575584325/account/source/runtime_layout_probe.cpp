#include <stdint.h>
#include <stddef.h>
#include <stdio.h>
#define SHARE_MEMORY_THREAD_NUM 100
#define SHARE_MEMORY_ARRAY_SIZE 3964
typedef struct Sched_Info {
	uint64_t time;										// the execution time of the program (nsec)
	unsigned int N;										// number of threads concerned
	unsigned int M;										// number of kep points per thread
	unsigned int TestedBounds;							// It took several period in testing engine
	//unsigned int tupleScheduling;						// now considering tuple scheduling :1, otherwise: 0; Then it save the hash ID of first touched key point
	uint16_t kpNumArray[SHARE_MEMORY_THREAD_NUM];		// the specific kpNum of each My_tid Thread, only consider almost 10 thread
	uint16_t kp[SHARE_MEMORY_ARRAY_SIZE];				// how many times should a thread yield before a kp
	uint16_t kpLoc[SHARE_MEMORY_ARRAY_SIZE];			// the hash ID of Key Point
	uint16_t kpOrder[SHARE_MEMORY_ARRAY_SIZE];			// recored the order of key points
} sched_info;
int main(){printf("{\"sizeof\":%zu,\"offsets\":{\"time\":%zu,\"N\":%zu,\"M\":%zu,\"TestedBounds\":%zu,\"kpNumArray\":%zu,\"kp\":%zu,\"kpLoc\":%zu,\"kpOrder\":%zu}}\n",sizeof(sched_info),offsetof(sched_info,time),offsetof(sched_info,N),offsetof(sched_info,M),offsetof(sched_info,TestedBounds),offsetof(sched_info,kpNumArray),offsetof(sched_info,kp),offsetof(sched_info,kpLoc),offsetof(sched_info,kpOrder));return 0;}
