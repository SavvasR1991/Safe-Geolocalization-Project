#include "Master_Station.h"


int Master_Station::create_master_station(struct ids_connections *conn,int bs){
    cout<<"--- Create Master station: "<<getpid()<<"\n";
    id = 'M';
    for(int k=0;k<1024;k++){
        buffer[k]=0;
        buffer1[k]=0;
        buffer2[k]=0;
        buffer3[k]=0;
        buffer4[k]=0;
    }
    addrlen  = sizeof(address);
    addrlen1 = sizeof(address1);
    addrlen2 = sizeof(address2);
    addrlen3 = sizeof(address3);
    addrlen4 = sizeof(address4);
    for(int i=0;i<9;i++){
        if(conn[i].from == 'M'){
            cout<<"----- Master: "<<getpid()<<" get socket "<<conn[i].port<<" to "<< conn[i].to<<"\n";
            if(conn[i].to=='A'){
                port_A = conn[i].port;
            }
            else if(conn[i].to =='B'){
                port_B = conn[i].port;
            }
            else if(conn[i].to =='C'){
                port_C = conn[i].port;
            }
            else if(conn[i].to =='D'){
                port_D = conn[i].port;
            }
            else{
                return -1;
            }
        }
        if(conn[i].to == 'M' && conn[i].from == 'X'){
            cout<<"----- Master: "<<getpid()<<" get socket "<<conn[i].port<<" to "<< conn[i].from<<"\n";
            port_X = conn[i].port;
        }
    }
    sem_START_PROCESSES    = semget(SEM_START_PROCESSES   ,1,PERMS|IPC_CREAT);
    sem_PREPARED_PROCESSES = semget(SEM_PREPARED_PROCESSES,1,PERMS|IPC_CREAT);

    server_fd = create_socket(); 
    setsockopt_socket_server(server_fd,&address,port_A);
    bind_socket_server(server_fd,&address,addrlen);
    listen_socket_server(server_fd);

    server_fd1 = create_socket(); 
    setsockopt_socket_server(server_fd1,&address1,port_B);
    bind_socket_server(server_fd1,&address1,addrlen1);
    listen_socket_server(server_fd1);
    
    server_fd2 = create_socket(); 
    setsockopt_socket_server(server_fd2,&address2,port_C);
    bind_socket_server(server_fd2,&address2,addrlen2);
    listen_socket_server(server_fd2);
    
    if(bs == 4){
        server_fd3 = create_socket(); 
        setsockopt_socket_server(server_fd3,&address3,port_D);
        bind_socket_server(server_fd3,&address3,addrlen3);
        listen_socket_server(server_fd3);
    }

    server_fd4 = create_socket(); 
    setsockopt_socket_server(server_fd4,&address4,port_X);
    bind_socket_server(server_fd4,&address4,addrlen4);
    listen_socket_server(server_fd4);

    cout<<"--- Ready Master: "<<getpid()<<"\n";
    return 0;
}

int Master_Station::start_master_station(int bs){
    
    up(sem_PREPARED_PROCESSES);
    down(sem_START_PROCESSES);
    up(sem_START_PROCESSES);
    
    cout<<"--- Start Master: "<<getpid()<<"\n";

    bool stop  = false;
    bool stop1 = false;
    bool stop2 = false;
    bool stop3 = false;
    bool stop4 = false;
    if(bs == 3)
        stop3 = true;
    new_socket  = accept_socket_server(server_fd ,&address ,addrlen);
    new_socket1 = accept_socket_server(server_fd1,&address1,addrlen1);
    new_socket2 = accept_socket_server(server_fd2,&address2,addrlen2);
    if(bs == 4)
        new_socket3 = accept_socket_server(server_fd3,&address3,addrlen3);
    new_socket4 = accept_socket_server(server_fd4,&address4,addrlen4);
    while(true){
        if(strcmp(buffer, "END     ")!=0 ){
            recv( new_socket , buffer, 1024,0); 
        }
        else{stop =true;}

        if(strcmp(buffer1, "END     ")!=0 ){
            recv( new_socket1 , buffer1, 1024,0); 
        }
        else{stop1 =true;}

        if(strcmp(buffer2, "END     ")!=0 ){
            recv( new_socket2 , buffer2, 1024,0); 
        }
        else{stop2 =true;}
        if(bs == 4)
            if(strcmp(buffer3, "END     ")!=0 ){
                recv( new_socket3 , buffer3, 1024,0); 
            }
        else{stop3 =true;}
        
        if(strcmp(buffer4, "END     ")!=0 ){
            recv( new_socket4 , buffer4, 1024,0); 
        }
        else{stop4 =true;}
        if(stop == true && stop1 == true && stop2 == true && stop3== true && stop4 == true){
            break;
        }
        send(new_socket4 , "From M  " , strlen("From M  ") , 0 ); 
    }
    close_socket_server(new_socket );
    close_socket_server(new_socket1);
    close_socket_server(new_socket2);
    if(bs == 4)
        close_socket_server(new_socket3);
    close_socket_server(new_socket4);
    cout<<"--- Delete Master station: "<<getpid()<<"\n";
    return 0;
}
