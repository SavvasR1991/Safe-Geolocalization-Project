#include <iostream>
#include <cstdlib>

class List {
	public:
		int totalNodes;

		struct Coordinates {
			int x;
			int y;
			int z;
		};

		struct Node2 {
			Coordinates* data;
			int* dataArray;
			struct Node2* next;
		};
		struct Node2* head = NULL;
		struct Node2* current = NULL;


		List(){
			totalNodes = 0;
		};
		void insert(int* dataArray) {
		    struct Node2* new_Node2 = (struct Node2*) malloc(sizeof(struct Node2));
			new_Node2->dataArray = dataArray;
			new_Node2->next = NULL;

			if (head == NULL) {
				head = new_Node2;
				current = head;
			}
			else {
				current->next = new_Node2;
				current = new_Node2;
			}

			totalNodes++;
		
		}
		void insert(int _x, int _y, int _z) {
			struct Node2* new_Node2 = (struct Node2*) malloc(sizeof(struct Node2));
			new_Node2->data = new Coordinates;
			new_Node2->data->x = _x;
			new_Node2->data->y = _y;
			new_Node2->data->z = _z;
			new_Node2->next = NULL;

			if (head == NULL) {
				head = new_Node2;
				current = head;
			}
			else {
				current->next = new_Node2;
				current = new_Node2;
			}

			totalNodes++;
		}

		void displayList() {
			struct Node2* ptr;
			ptr = head;

			while (ptr != NULL) {
				std::cout << ptr->data->x << " " << ptr->data->y << " " << ptr->data->z << "\n";
				ptr = ptr->next;
			}
		}

		void convertListToArray(int** arrayInput) {
			struct Node2* ptr;
			int rowIndex = 0;;
			ptr = head;
			while (ptr != NULL) {
				arrayInput[rowIndex][0] = ptr->data->x;
				arrayInput[rowIndex][1] = ptr->data->y;
				arrayInput[rowIndex][2] = ptr->data->z;
				rowIndex++;
				ptr = ptr->next;
			}

		}
		void deleteList() {
			struct Node2* ptr;
			struct Node2* ptr2;
			ptr = head;
			head = NULL;
			totalNodes = 0;
			while (ptr != NULL) {
				ptr2 = ptr;
				delete ptr->data;
				ptr = ptr->next;
				delete ptr2;
			}
		}
};
