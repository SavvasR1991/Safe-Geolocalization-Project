#ifndef BASE_STATIONS_H
#define	BASE_STATIONS_H

#include "Operations.h"
#include <netinet/in.h>

using namespace std;

////////////////
//  BS CLASS  //
////////////////

class Base_Stations
{
    private:
        int sem_START_PROCESSES;
        int sem_PREPARED_PROCESSES;
        int sock; 
        int server_fd, new_socket; 
        int addrlen;    
        int port_Master;
        int port_X;
        char id;
        char buffer[1024]; 
        char *hello; 
        struct sockaddr_in serv_addr; 
        struct sockaddr_in address; 
    public:
        int create_base_station(struct ids_connections *,char);
        int start_base_station();
};

#endif
