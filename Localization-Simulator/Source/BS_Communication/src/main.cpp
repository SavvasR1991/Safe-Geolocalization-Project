#include <stdio.h> 
#include <sys/socket.h> 
#include <arpa/inet.h> 
#include <unistd.h> 
#include <string.h> 
#include <stdlib.h> 
#include <sys/wait.h>
#include <sys/sem.h>
#include <sys/time.h> 
#include <bits/stdc++.h> 
#include <iostream>
#include <fstream>

#include "Node_X.h"
#include "Base_Stations.h"
#include "Master_Station.h"
#include "Operations.h"

#define GetCurrentDir getcwd
std::string GetCurrentWorkingDir( void ) {
    char buff[FILENAME_MAX];
    GetCurrentDir( buff, FILENAME_MAX );
    std::string current_working_dir(buff);
    current_working_dir[current_working_dir.length()-6] = '\0';
    current_working_dir.erase (current_working_dir.end()-6, current_working_dir.end());
    return current_working_dir.append("/Total_Time.txt");
}

using namespace std;

int main(int argc, char const *argv[]) 
{ 
    cout<<"-> Set up enviroment\n";
    if(argc!=3){
        cout<<"-> Wrong arguments\n";
        return -1;
    }
    int status = 0;
    int i = 0,j=0;
    int sem_START_PROCESSES;
    int sem_PREPARED_PROCESSES;
    int total_bs = atoi(argv[1]);
    int steps = atoi(argv[2]);

    int *bs_pid = new int[total_bs+1];
    double time_taken; 
    char ids [4] = {'A', 'B', 'C', 'D'};

    Base_Stations BSs;
    Node_X nodeX;
    Master_Station master;
    pid_t pid_bs, wpid, pid_node_x, pid_master;
    senum arg;
    
    struct timeval start, end; 
    struct ids_connections conn[9] = {
        { 'X','A',9474 },
        { 'X','B',9475 },
        { 'X','C',9476 },
        { 'X','D',9477 },
        { 'X','M',9478 },
        { 'M','A',9479 },
        { 'M','B',9480 },
        { 'M','C',9481 },
        { 'M','D',9482 }
    };
      
    //Initialize semophores//
    sem_PREPARED_PROCESSES = semget(SEM_PREPARED_PROCESSES,1,PERMS|IPC_CREAT);             
    arg.val=0;                                                       
    semctl(sem_PREPARED_PROCESSES,0,SETVAL,arg);

    sem_START_PROCESSES = semget(SEM_START_PROCESSES,1,PERMS|IPC_CREAT);             
    arg.val=0;                                                       
    semctl(sem_START_PROCESSES,0,SETVAL,arg);
    
    for (j =0;j<9;j++){
        cout<<"-- Set sockets: "<<conn[j].from<<conn[j].to<<" "<<conn[j].port<<"\n";
    }
    
    //Initialize processes//
    for (i=0;i<total_bs;i++){
        pid_bs = fork();
        if (pid_bs == 0){
            if(BSs.create_base_station(conn,ids[i]) == 0){
                if (BSs.start_base_station() == 0){
                    return 0;
                }else{ 
                    return -1;
                }
            }else{
                return -1;
            }
        }
        else{
            bs_pid[i] = pid_bs;
        }
    }
    pid_node_x = fork();
    if (pid_node_x == 0){
        if(nodeX.create_Node_X(conn,total_bs) == 0){
            if (nodeX.start_Node_X(steps,total_bs) == 0){
                return 0;
            }else{ 
                return -1;
            }
        }else{
            return -1;
        }
    }
    else{
        bs_pid[i] = pid_node_x;
        i++;
    }

    pid_master = fork();
    if (pid_master == 0){
        if(master.create_master_station(conn,total_bs) == 0){
            if (master.start_master_station(total_bs) == 0){
                return 0;
            }else{ 
                return -1;
            }
        }else{
            return -1;
        }
    }
    else{
        bs_pid[i] = pid_node_x;
    }

    cout<<"-> Preparing base stations....\n";
    total_bs = total_bs + 2;
    for (i=0;i<total_bs;i++){
         down(sem_PREPARED_PROCESSES);
    }
    
    //Start processes//
    cout<<"-> Start simulation\n";
    
    gettimeofday(&start, NULL); 
    ios_base::sync_with_stdio(false); 
    up(sem_START_PROCESSES);

    while ((wpid = wait(&status)) > 0){
        if(status > 0){
            cout<<"-> Error occured in simulation in process:"<<wpid<<" ...!!! Abort....\n";
            for (i=0;i<total_bs;i++){
                cout<<"  Closing :"<<bs_pid[i]<<"....\n";
                kill(bs_pid[i], SIGKILL);
            }
            semctl(sem_START_PROCESSES,1,IPC_RMID,0);
            semctl(sem_PREPARED_PROCESSES,1,IPC_RMID,0);

            return -1;
        }
    };
    cout<<"-> Stop simulation\n";
    gettimeofday(&end, NULL); 
    time_taken = (end.tv_sec - start.tv_sec) * 1e6; 
    time_taken = (time_taken + (end.tv_usec - start.tv_usec)) * 1e-6; 
    
    semctl(sem_START_PROCESSES,1,IPC_RMID,0);
    semctl(sem_START_PROCESSES,1,IPC_RMID,0);

    ofstream myfile (GetCurrentWorkingDir().c_str());
    if (myfile.is_open())
    {
        myfile <<time_taken;
        myfile.close();
    }
    cout << "Time taken by program is : " << time_taken << " sec" << endl; 
    return 0; 
} 
