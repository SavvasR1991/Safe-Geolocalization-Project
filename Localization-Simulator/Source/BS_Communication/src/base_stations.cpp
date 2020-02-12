#include "Base_Stations.h"
#include "Operations.h"


int Base_Stations::create_base_station(struct ids_connections *conn,char ids){

    cout<<"--- Create base station "<<ids<<": "<<getpid()<<"\n";
    id = ids;
    int connection=1;
    addrlen = sizeof(address);
    for(int k=0;k<1024;k++){buffer[k]=0;}
    for(int i=0;i<9;i++){
        if(conn[i].to == ids){
            cout<<"----- BS "<<ids<<": "<<getpid()<<" get socket "<<conn[i].port<<" from "<< conn[i].from<<"\n";
            if(conn[i].from == 'M'){
                port_Master =conn[i].port;
            }
            else if(conn[i].from == 'X'){
                port_X =conn[i].port;
            }
            else{
                return -1;
            }
        }
    }

    sem_START_PROCESSES = semget(SEM_START_PROCESSES,1,PERMS|IPC_CREAT);
    sem_PREPARED_PROCESSES = semget(SEM_PREPARED_PROCESSES,1,PERMS|IPC_CREAT);

    sock = create_socket();     
    set_address_socket_client(&serv_addr,port_Master);
    
    server_fd = create_socket(); 
    setsockopt_socket_server(server_fd,&address,port_X);
    bind_socket_server(server_fd,&address,addrlen);
    listen_socket_server(server_fd);

    while(connection == 1){
        connection = connect_socket_client(sock,&serv_addr,sizeof(serv_addr));
    }
    cout<<"--- Ready Node "<<id<<": "<<getpid()<<"\n";
    return 0;
}

int Base_Stations::start_base_station(){
    
    up(sem_PREPARED_PROCESSES);
    down(sem_START_PROCESSES);
    up(sem_START_PROCESSES);
    
    cout<<"--- Start Node "<<id<<": "<<getpid()<<"\n";
    new_socket = accept_socket_server(server_fd,&address,addrlen);
    char mess[] = "From d  "; 
    mess[5] = id;
    while(true){
        recv( new_socket , buffer, 1024,0); 
        if(strcmp(buffer, "END     ")==0){
            break;
        }
        send(sock , mess , strlen(mess) , 0 ); 
    }
    send(sock , "END     " , strlen("END     ") , 0 ); 
    close_socket_server(new_socket);
    cout<<"--- Delete base station "<<id<<": "<<getpid()<<"\n";
    return 0;
}
