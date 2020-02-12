#include "Operations.h"

struct sembuf inc[1] = {0,1,0};

struct sembuf dec[1] = {0,-1,0};

void up(int semid)
{
    semop(semid,&inc[0],1);
}

void down(int semid)
{
    semop(semid,&dec[0],1);
}


int create_socket()
{
    int sock = 0;
    if ((sock = socket(AF_INET, SOCK_STREAM, 0)) < 0) 
    { 
        printf("\n Socket creation error \n"); 
        exit(EXIT_FAILURE); 
    } 
    
    return sock;
}

void set_address_socket_client(struct sockaddr_in* serv_addr, int PORT)
{
    serv_addr->sin_family = AF_INET; 
    serv_addr->sin_port = htons(PORT); 
    if(inet_pton(AF_INET, "127.0.0.1", &serv_addr->sin_addr)<=0)  
    { 
        printf("\nInvalid address/ Address not supported \n"); 
        exit(EXIT_FAILURE); 
    } 

}

int connect_socket_client(int sock, struct sockaddr_in* serv_addr,int size)
{
    if (connect(sock, (struct sockaddr *)serv_addr, size) < 0) 
    { 
        return 1;
    } 
    return 0;
}

void setsockopt_socket_server(int server_fd, struct sockaddr_in * address, int PORT)
{
    int opt = 1; 
    if (setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR | SO_REUSEPORT,&opt, sizeof(opt))) 
    { 
        printf("\n Socket setsockopt error \n"); 
        exit(EXIT_FAILURE); 
    } 
    address->sin_family = AF_INET; 
    address->sin_addr.s_addr = INADDR_ANY; 
    address->sin_port = htons( PORT ); 
}

void bind_socket_server(int server_fd,struct sockaddr_in * address,int size)
{
    if (bind(server_fd, (struct sockaddr *)address,size)<0) 
    { 
        printf("\n Socket bind error \n"); 
        exit(EXIT_FAILURE); 
    } 
}

void listen_socket_server(int server_fd)
{
    if (listen(server_fd, 3) < 0) 
    { 
        printf("\n Socket listen error \n"); 
        exit(EXIT_FAILURE); 
    } 
}

int accept_socket_server(int server_fd,struct sockaddr_in * address,int addrlen)
{
    int new_socket = 0;
    if ((new_socket = accept(server_fd, (struct sockaddr *)address,(socklen_t*)&addrlen))<0) 
    { 
        printf("\n Socket accept error \n"); 
        exit(EXIT_FAILURE); 
    } 
    return new_socket;
}

int close_socket_server(int server_fd){
    return close(server_fd); 
}

