#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <stdbool.h>
#include <stdlib.h>
#include <signal.h>
#include <time.h>
#define TIMEOUT 60

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
	if(ret <= 0){
		puts("read error");
		_exit(1);
	}
	if(buf[ret-1] == '\n')
		buf[ret-1] = '\x00';
} 

void menu(){
	puts("$$$$$$$$$$$$$$$$$$$$$$$$");
	puts("  Return of seethefile  ");
	puts("$$$$$$$$$$$$$$$$$$$$$$$$");
	puts("  1. Open               ");
	puts("  2. Read               ");
	puts("  3. Write              ");
	puts("  4. Allocate           ");
    puts("  5. Exit               ");
	puts("$$$$$$$$$$$$$$$$$$$$$$$$");
	printf("Your choice :");
}
FILE *fp = NULL ;
FILE *fp_list[3];
char *content ;
void openfile(){
	char filename[0x30];
	memset(filename,0,0x30);
	for(int i = 0 ; i < 3 ; i++){
		if(!fp_list[i]){	
			printf("Filnename:");
			read_input(filename,0x2f);
			if(strstr(filename,"flag")){
				puts("No ! ");
				exit(0);
			}
			fp_list[i] = fopen(filename,"r");
			if(fp_list[i])
				puts("Good ");
			else
				puts("Bad :(");
			return;
		}
	}		
}


void readfile(){
	size_t size; 
	unsigned int idx;
	printf("Index:");
	idx = read_long();
	if(idx < 0 || idx >= 3)
		exit(-1);
	if(!content){
		puts("You need to allocate a buf first !");
		return ;
	}
	if(fp_list[idx]){
		printf("Size:");
		size = read_long();
		fread(content,size,1,fp_list[idx]);
		puts("Done !");
	}
	else{
		puts("You need to open file first !");	
	}
}

void writefile(){
	if(!content){
		puts("You need to allocate a buf first !");
		return ;
	}
	if(!fp){
		fp = fopen("/dev/null","w");
		
		if(!fp)
			exit(-1);
		if(strstr(content,"FLAG")){
			puts("danger !");
			exit(0);
		}
	}
	if(content)
		fwrite(content,1,1,fp);
}

void allocate(){
	size_t size ;
	printf("Size:");
	size = read_long();
	content = malloc(size);
}

int main(){
	init_proc();
	while(1){
		menu();
		switch(read_long()){
			case 1 :
				openfile();
				break ;
			case 2 :
				readfile();
				break ;
			case 3 :
				writefile();
				break;
			case 4 :
				allocate();
				break;
			case 5 :
				free(content);
				for(int i = 0 ; i < 3 ; i++){
					if(fp_list[i])
						fclose(fp_list[i]);
				}
				if(fp)
					fclose(fp);
				exit(0);
				break ;
			default :
				puts("Invalid choice");
				break;
		}
	}
}



