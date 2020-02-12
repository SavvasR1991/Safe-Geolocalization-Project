#ifndef NODE_X_H
#define	NODE_X_H

#include <iostream>
#include <netinet/in.h>

using namespace std;

////////////////////
//  NODE X CLASS  //
////////////////////

class Node_X
{
    private:
        int sem_START_PROCESSES;
        int sem_PREPARED_PROCESSES;
        int sock; 
        int sock1; 
        int sock2; 
        int sock3; 
        int sock4; 
        int port_A;
        int port_B;
        int port_C;
        int port_D;
        int port_M;
        char buffer[1024]; 
        struct sockaddr_in serv_addr;  
        struct sockaddr_in serv_addr1; 
        struct sockaddr_in serv_addr2;
        struct sockaddr_in serv_addr3; 
        struct sockaddr_in serv_addr4;
    public:
        int create_Node_X(struct ids_connections *conn,int);
        int start_Node_X(int,int);
};

#endif
