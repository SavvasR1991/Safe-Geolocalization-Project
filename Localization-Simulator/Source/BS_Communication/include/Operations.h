#ifndef OPERATIONS_H
#define OPERATIONS_H

#include <sys/sem.h>
#include <sys/ipc.h>
#include <sys/types.h>
#include <string.h>
#include <iostream>
#include <unistd.h>
#include <string.h>
#include <stdio.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <stdlib.h> 
#include <netinet/in.h>
#include <netinet/tcp.h>
#include <netdb.h>

#define SEM_START_PROCESSES (key_t) 4214
#define SEM_PREPARED_PROCESSES (key_t) 4213

#define PERMS 0666

struct ids_connections
{
    char from;
    char to;
    int port;
};

union senum
{
    int val;
    struct semid *buf;
    unsigned short *semarray;
};

void down(int);
void up(int);

int create_socket();
void set_address_socket_client(struct sockaddr_in* serv_addr, int PORT);
int connect_socket_client(int sock, struct sockaddr_in* serv_addr,int size);
void setsockopt_socket_server(int server_fd, struct sockaddr_in * address, int PORT);
void bind_socket_server(int server_fd,struct sockaddr_in * address,int size);
void listen_socket_server(int server_fd);
int accept_socket_server(int server_fd,struct sockaddr_in * address,int addrlen);
int close_socket_server(int server_fd);

#endif
