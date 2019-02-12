#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <stdbool.h>
#include <stdlib.h>
#include <signal.h>
#include <time.h>
#define TIMEOUT 60
#define MAX 11


bool is_create = false;
void handler(int signum){
	puts("Timeout");
	_exit(1);
} 

void init_proc(){
	setvbuf(stdin,0,2,0);
	setvbuf(stdout,0,2,0);
	setvbuf(stderr,0,2,0);
	signal(SIGALRM,handler);
	alarm(TIMEOUT);
} 

long long read_long(){
	char buf[24];
	long long choice ;
	__read_chk(0,buf,23,24);
	choice = atoll(buf);
	return choice;
}
 
void read_input(char *buf,unsigned int size){
	int ret ;
	ret = __read_chk(0,buf,size,size);
	if(ret < 0){
		puts("read error");
		_exit(1);
	}
	if(buf[ret-1] == '\n')
		buf[ret-1] = '\x00';
} 

void menu(){
	puts("***********************");
	puts("     Heap Paridise     ");
	puts("***********************");
	puts(" 1. Allocate           ");
	puts(" 2. Free               ");
	puts(" 3. Create the Paridise");
	puts(" 4. Exit               ");
	puts("***********************");
	printf("You Choice:");
}

char *heap[MAX];

void allocate(){
	size_t size = 0 ;
	for(int i = 0 ; i <= MAX ; i++){
		if(!heap[i]){
			printf("Size :");
			size = read_long();
			if(size <= 0x78){
				heap[i] = malloc(size);
				if(!heap[i]){
					puts("Error!");
					_exit(-1);
				}
				printf("Data :");
				read_input(heap[i],size);
			}

			return ;
		}
	}
	puts("You can't allocate anymore !");
	return ;	
}

void del(){
	long long idx ;
	printf("Index :");
	idx = read_long();
	if(idx <= MAX)
		free(heap[idx]);
}

void paridise(){
	if(!is_create){
		malloc(0x21000);
		puts(":)");
		is_create = true;
	}
	return ;	
}

int main(){
	init_proc();
	while(1){
		menu();
		switch(read_long()){
			case 1 :
				allocate();
				break;
			case 2 :
				del();
				break;
			case 3 :
				paridise();
				break;
			case 4 :
				_exit(0);
			default: 
				puts("Invalid Choice !");
				break;
		}
	}
	return 0 ;
}
