#ifndef list_H_
#define list_H_

/*  A classic doubly linked list.

    List interface:
*/

typedef struct list list_t;
typedef struct list_iter list_iter_t;


/*  Creates a new list.
*/
list_t *list_create();

/*  Destroys the given list.
*/
void list_destroy(list_t *list);

/*  Returns the current size of the given list.
*/
int list_size(list_t *list);

/*  Adds the given element to the start of the given list.
*/
void list_addfirst(list_t *list, void *elem);

/*  Adds the given element to the end of the given list.
*/
void list_addlast(list_t *list, void *elem);

/*  Interface for iterator
*/
/*  Creates a new list iterator for iterating over the given list.
 */
list_iter_t *list_createiter(list_t *list);

/*  Destroys the given list iterator.
 */
void list_destroyiter(list_iter_t *iter);

/*  Returns 0 if the given list iterator has reached the end of the
    list, or 1 otherwise.
 */
int list_hasnext(list_iter_t *iter);

/*  Returns the next element in the sequence represented by the given
    list iterator.
 */
void *list_next(list_iter_t *iter);

#endif list_H_