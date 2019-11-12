#include <iostream>
#include <cstdlib>

struct Node
 {
	int** data;
	int totalRows;
	struct Node* next;
};

class List2 {
	public:

		
		struct Node* head = NULL;
		struct Node* current = NULL;


		void insert(int** arrayInput,int totalRows) {
			struct Node* new_node = (struct Node*) malloc(sizeof(struct Node));
			new_node->data = arrayInput;
			new_node->next = NULL;
			new_node->totalRows = totalRows;
			if (head == NULL) {
				head = new_node;
				current = head;
			}
			else {
				current->next = new_node;
				current = new_node;
			}

		}

		void displayList() {
			struct Node* ptr;
			int i, j;
			ptr = head;

			while (ptr != NULL) {
				for (i = 0; i < ptr->totalRows; ++i) {
					for (j = 0; j < 3; ++j) {
						std::cout << ptr->data[i][j] << " ";

					}
					std::cout << "\n";
				}
				ptr = ptr->next;
				std::cout << "\n";

			}
		}

		void deleteList() {
			struct Node* ptr;
			struct Node* ptr2;
			int i,j;

			ptr = head;
			head = NULL;
			while (ptr != NULL) {
				ptr2 = ptr;
				for (i = 0; i < ptr->totalRows; ++i) {
					delete[] ptr->data[i];
				}
				delete ptr->data;
				ptr = ptr->next;
				delete ptr2;
			}
		}

};
