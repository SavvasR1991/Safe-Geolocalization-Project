#include "Node_X.h"
#include "Operations.h"
#include <sys/types.h>
#include <unistd.h>

int Node_X::create_Node_X(struct ids_connections *conn, int bs){
    sem_START_PROCESSES = semget(SEM_START_PROCESSES,1,PERMS|IPC_CREAT);
    sem_PREPARED_PROCESSES = semget(SEM_PREPARED_PROCESSES,1,PERMS|IPC_CREAT);
    cout<<"--- Create Node X: "<<getpid()<<"\n";
    int connection=1,connection1=1,connection2=1,connection3=1,connection4=1;
    for(int k=0;k<1024;k++){ buffer[k]=0;}
    for(int i=0;i<9;i++){
        if(conn[i].from == 'X'){
            cout<<"----- Node X: "<<getpid()<<" get socket "<<conn[i].port<<" from "<< conn[i].to<<"\n";
            if(conn[i].to == 'M'){
                port_M =conn[i].port;
            }
            else if(conn[i].to == 'A'){
                port_A =conn[i].port;
            }
            else if(conn[i].to == 'B'){
                port_B =conn[i].port;
            }
            else if(conn[i].to == 'C'){
                port_C =conn[i].port;
            }
            else if(conn[i].to == 'D'){
                port_D =conn[i].port;
            }
            else{
                return -1;
            }
        }
    }
    sock = create_socket();     
    set_address_socket_client(&serv_addr ,port_M);
    sock1 = create_socket();     
    set_address_socket_client(&serv_addr1,port_A);
    sock2 = create_socket();     
    set_address_socket_client(&serv_addr2,port_B);
    sock3 = create_socket();     
    set_address_socket_client(&serv_addr3,port_C);
    if(bs == 4)
        sock4 = create_socket();     
        set_address_socket_client(&serv_addr4,port_D);

    while(connection == 1){
        connection  = connect_socket_client(sock ,&serv_addr, sizeof(serv_addr));
    }
    while(connection1 == 1){ 
        connection1 = connect_socket_client(sock1,&serv_addr1,sizeof(serv_addr1));
    }
    while(connection2 == 1){
        connection2 = connect_socket_client(sock2,&serv_addr2,sizeof(serv_addr2));
    }
    while(connection3 == 1){
        connection3 = connect_socket_client(sock3,&serv_addr3,sizeof(serv_addr3));
    }
    if(bs == 4)
        while(connection4 == 1){
            connection4 = connect_socket_client(sock4,&serv_addr4,sizeof(serv_addr4));
        }
    cout<<"--- Ready Node X: "<<getpid()<<"\n";
    return 0;
}

int Node_X::start_Node_X(int steps, int bs){

    up(sem_PREPARED_PROCESSES);
    down(sem_START_PROCESSES);
    up(sem_START_PROCESSES);
    
    int counter = 1;
    cout<<"--- Start Node X: "<<getpid()<<"\n";
    for(int i=0;i<steps;i++){
        send(sock1 , "From X  " , strlen("From X  ") , 0 ); 
        send(sock2 , "From X  " , strlen("From X  ") , 0 ); 
        send(sock3 , "From X  " , strlen("From X  ") , 0 ); 
        if(bs == 4)
            send(sock4 , "From X  " , strlen("From X  ") , 0 ); 
        send(sock  , "From X  " , strlen("From X  ") , 0 ); 
        recv(sock  , buffer , 1024, 0); 
    }
    send(sock  , "END     " , strlen("END     ") , 0 ); 
    send(sock1 , "END     " , strlen("END     ") , 0 ); 
    send(sock2 , "END     " , strlen("END     ") , 0 ); 
    send(sock3 , "END     " , strlen("END     ") , 0 ); 
    if(bs == 4)
        send(sock4 , "END     " , strlen("END     ") , 0 ); 
    cout<<"--- Delete Node X: "<<getpid()<<"\n";
    return 0;
}
