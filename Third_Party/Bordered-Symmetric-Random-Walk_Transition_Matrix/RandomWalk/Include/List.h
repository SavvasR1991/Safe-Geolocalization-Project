#include <iostream>

class List {
	public:
		struct Coordinates {
			int x;
			int y;
			int z;
		};

		struct Node {
			Coordinates* data;
			struct Node* next;
		};
		struct Node* head = NULL;
		struct Node* current = NULL;

		int totalNodes = 0;

		void insert(int _x, int _y, int _z) {
			struct Node* new_node = (struct Node*) malloc(sizeof(struct Node));
			new_node->data = new Coordinates;
			new_node->data->x = _x;
			new_node->data->y = _y;
			new_node->data->z = _z;
			new_node->next = NULL;

			if (head == NULL) {
				head = new_node;
				current = head;
			}
			else {
				current->next = new_node;
				current = new_node;
			}

			totalNodes++;
		}

		void displayList() {
			struct Node* ptr;
			ptr = head;

			while (ptr != NULL) {
				std::cout << ptr->data->x << " " << ptr->data->y << " " << ptr->data->z << "\n";
				ptr = ptr->next;
			}
		}

		void convertListToArray(int** arrayInput) {
			struct Node* ptr;
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
			struct Node* ptr;
			struct Node* ptr2;
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