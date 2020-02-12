#ifndef MASTER_STATION_H
#define	MASTER_STATION_H

#include "Operations.h"
#include <netinet/in.h>

using namespace std;

////////////////
//  BS CLASS  //
////////////////

class Master_Station
{
    private:
        int sem_START_PROCESSES;
        int sem_PREPARED_PROCESSES;
        char id;

        int server_fd, new_socket; 
        struct sockaddr_in address; 
        int addrlen; 
        char buffer[1024];
        
        int server_fd1, new_socket1; 
        struct sockaddr_in address1; 
        int addrlen1; 
        char buffer1[1024];
        
        int server_fd2, new_socket2; 
        struct sockaddr_in address2; 
        int addrlen2; 
        char buffer2[1024]; 
        
        int server_fd3, new_socket3; 
        struct sockaddr_in address3; 
        int addrlen3; 
        char buffer3[1024]; 
        
        int server_fd4, new_socket4; 
        struct sockaddr_in address4; 
        int addrlen4; 
        char buffer4[1024]; 

        int port_A;
        int port_B;
        int port_C;
        int port_D;
        int port_X;

    public:
        int create_master_station(struct ids_connections *,int);
        int start_master_station(int);

};

#endif
