#include "list.h"

#include <stdlib.h>
#include <stdio.h>

/*  Nodes for the list.
*/
typedef struct listnode listnode_t;

struct listnode {
    listnode_t *next;
    listnode_t *prev;
    void *elem;
};

struct list {
    listnode_t *head;
    listnode_t *tail;
    int size;
};

struct list_iter {
    listnode_t *node;
};
//  Internal node-interface:

/*  Create a new node containing the given element.
    Returns NULL on failure.
*/
listnode_t *newnode(void *elem){
    listnode_t *node = malloc(sizeof(listnode_t));
    if (!node){
        printf("Error in newnode()");
        return NULL;
    }
    node->next = NULL;
    node->prev = NULL;
    node->elem = elem;
    return node;
}


/*  Creates an empty list and returns the pointer.
    Returns NULL on failure.
*/
list_t *list_create(){
    list_t *newlist = malloc(sizeof(list_t));
    if (!newlist){
        printf("Error in list_create()");
        return NULL;
    }
    newlist->head = NULL;
    newlist->tail = NULL;
    newlist->size = 0;
    return newlist;
}

/*  Go through the list and destroy all elements before
    freeing the list itself.
*/
void list_destroy(list_t *list){
    listnode_t *node = list->head;
    // First free all nodes...
    while (node != NULL){
	    listnode_t *tmp = node;
	    node = node->next;
	    free(tmp);
    }
    // ...then the list.
    free(list);
}
/*  Get current size.
*/
int list_size(list_t *list){
    return list->size;
}

/*  Insert the given element first in the list.
*/
void list_addfirst(list_t *list, void *elem){
    listnode_t *node = newnode(elem);
    if(!list->head){
        list->head = list->tail = node;
    } else {
        list->head->prev = node;
        node->next = list->head;
        list->head = node;
    }
    list->size++;
}

/*  Insert the given element at the end of the list.
*/
void list_addlast(list_t *list, void *elem){
    listnode_t *node = newnode(elem);
    if (!list->head){
	    list->head = list->tail = node;
    } else {
	    list->tail->next = node;
	    node->prev = list->tail;
	    list->tail = node;
    }
    list->size++;
}

/*  Create an iterator on the given list.
*/
list_iter_t *list_createiter(list_t *list){
    list_iter_t *iter = malloc(sizeof(list_iter_t));
    if (!iter){
        printf("Error in list_createiter()");
        return NULL;
    }
    iter->node = list->head;
    return iter;
}

void list_destroyiter(list_iter_t *iter){
    free(iter);
}

int list_hasnext(list_iter_t *iter){
    if (!iter->node)
	    return 0;
    else
	    return 1;
}

/*  Return the next element in the list pointed to by
    the iterator.
*/
void *list_next(list_iter_t *iter){
    if (!iter->node){
        printf("List exhausted!");
        return NULL;
    } else {
	    void *elem = iter->node->elem;
	    iter->node = iter->node->next;
	    return elem;
    }
}
