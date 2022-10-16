// importing constants
import {
    CART_ADD_ITEM,
    CART_REMOVE_ITEM,
    CART_SAVE_SHIPPING_ADDRESS,
    CART_SAVE_PAYMENT_METHOD,
    CART_CLEAR_ITEMS,
} from '../constants/cartConstants'


// Reducers are the functions that contain logic and calculations that needed to be performed on the state
// according to action type passed by actions functions

// cart reducer that performs add items, remove items, clear items in cart and shipping address component
export const cartReducer = (state={cartItems:[], shippingAddress:[]}, action) => {
    switch (action.type) {
        // if action.type sent by action function == CART_ADD_ITEM
        case CART_ADD_ITEM:
            const item = action.payload // items added by users
            // check whether the item is already in cart or not
            const existItem = state.cartItems.find(x => x.product === item.product) 
            if(existItem){
                // if the item is already in cart
                return {
                    ...state, // spreading operator is used to make copy of the previous state except cart items
                    cartItems: state.cartItems.map(x => x.product === existItem.product ? item : x) // mapping existing item with updated quantity and other previously added items
                }
            } else {
                // if new item is added
                return {
                    ...state, // copy of the previous state except cart items
                    cartItems: [...state.cartItems, item] // mapping new item and other previously added items
                }
            }

        // if action.type sent by action function == CART_REMOVE_ITEM
        case CART_REMOVE_ITEM:
            return {
                ...state, // copy of the previous state except cart items
                cartItems: state.cartItems.filter(x => x.product !== action.payload) // mapping all items filtering the item to be removed
            }

        case CART_SAVE_SHIPPING_ADDRESS:
            return {
                ...state, // copy of the previous state except shipping address
                shippingAddress: action.payload // save shipping address given by user in a state
            }

        case CART_SAVE_PAYMENT_METHOD:
            return {
                ...state, // copy of the previous state except payment method
                paymentMethod: action.payload // save payment method given by user in a state
            }
        
        case CART_CLEAR_ITEMS:
            return {
                ...state, // copy of the previous state except cart items
                cartItems: [] // clear all cart items
            }

        // if action.type is none of above cases - return existing state
        default:
            return state
    }
}