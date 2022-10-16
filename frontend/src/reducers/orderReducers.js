// importing constants
import { 
    ORDER_CREATE_REQUEST,
    ORDER_CREATE_SUCCESS,
    ORDER_CREATE_FAIL,
    ORDER_CREATE_RESET,

    ORDER_DETAILS_REQUEST,
    ORDER_DETAILS_SUCCESS,
    ORDER_DETAILS_FAIL,

    ORDER_PAY_REQUEST,
    ORDER_PAY_SUCCESS,
    ORDER_PAY_FAIL,
    ORDER_PAY_RESET,

    ORDER_LIST_MY_REQUEST,
    ORDER_LIST_MY_SUCCESS,
    ORDER_LIST_MY_FAIL,
    ORDER_LIST_MY_RESET,
 } from '../constants/orderConstants'

// Reducers are the functions that contain logic and calculations that needed to be performed on the state
// according to action type passed by actions functions

// reducer to create new order and initializing orderCreate state as null
export const orderCreateReducer = (state={}, action) => {
    switch(action.type){
        // if action.type sent by action function == ORDER_CREATE_REQUEST
        case ORDER_CREATE_REQUEST:
            return {
                 loading: true // loading before api call
            }

        // when order create api request is succeeded    
        case ORDER_CREATE_SUCCESS:
            return {
                loading: false,
                success: true,
                order: action.payload // data fetched from api response
            }

        // if api response sends error    
        case ORDER_CREATE_FAIL:
            return {
                loading: false,
                error: action.payload // error message from api response
            }

        // this is called after order is placed    
        case ORDER_CREATE_RESET:
            return {}

        default:
            return state
    }
}

// reducer to fetch order details and initializing loading as true, order-items and shipping address as null
export const orderDetailsReducer = (state={loading: true, orderItems:[], shippingAddress:{}}, action) => {
    switch(action.type){
        // before api is called to fetch data
        case ORDER_DETAILS_REQUEST:
            return {
                ...state, // copy of the previous state
                loading: true
            }

        // after api fetch is succeeded    
        case ORDER_DETAILS_SUCCESS:
            return {
                loading: false, 
                order: action.payload // order details fetched from api response
            }

        // if api response sends error    
        case ORDER_DETAILS_FAIL:
            return {
                loading: false,
                error: action.payload // error message from api response
            }

        default:
            return state
    }
}


// reducer to pay the order
export const orderPayReducer = (state={}, action) => {
    switch(action.type){
        // before api is called to fetch data
        case ORDER_PAY_REQUEST:
            return {
                loading: true
            }

        // after api fetch is succeeded
        case ORDER_PAY_SUCCESS:
            return {
                loading: false,
                success: true
            }

        case ORDER_PAY_FAIL:
            return {
                loading: false,
                error: action.payload
            }

        case ORDER_PAY_RESET:
            return {}

        default:
            return state
    }
}


// reducer to list my orders with initialization of orders as null
export const orderListMyReducer = (state={orders:[]}, action) => {
    switch(action.type){
        case ORDER_LIST_MY_REQUEST:
            return {
                loading: true
            }

        // after api fetch is succeeded
        case ORDER_LIST_MY_SUCCESS:
            return {
                loading: false,
                orders: action.payload // list of orders fetched from api response
            }

        case ORDER_LIST_MY_FAIL:
            return {
                loading: false,
                error: action.payload // error message from api response
            }

        case ORDER_LIST_MY_RESET:
            return {
                orders: []
            }

        default:
            return state
    }
}