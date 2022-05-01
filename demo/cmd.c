// 简单的命令行实现

#include <stdio.h>
#include <string.h>
#include <stdlib.h>


#define MAX_BUF_SIZE 200
int main() {
	char buf[MAX_BUF_SIZE];
	while (1) {
		memset(buf, 0, MAX_BUF_SIZE);
		printf("diagnose> ");
		gets(buf);
		if (strlen(buf) < 2) {
			switch (buf[0]) {
				case 'q':
					exit(0);
					break;
				case '\n':
				case '\r':
				case '\t':
				case '\0':
					break;
				default:
					printf("output = %s\n", buf);
					break;
			}
		} else {
			printf("output = %s\n", buf);
		}

	}
	return 0;
}