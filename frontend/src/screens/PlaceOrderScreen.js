import React, { useState, useEffect } from 'react'
import { Row, Col, ListGroup, Image, Card, Button } from 'react-bootstrap'
import { Link } from 'react-router-dom'
import { useDispatch, useSelector } from 'react-redux'
import Message from '../components/Message'
import CheckoutSteps from '../components/CheckoutSteps'
import { createOrder } from '../actions/orderActions'
import { ORDER_CREATE_RESET } from '../constants/orderConstants'


function PlaceOrderScreen({ history }) {

    const orderCreate = useSelector(state => state.orderCreate)
    const {order, error, success} = orderCreate

    const cart = useSelector(state => state.cart)
    const { shippingAddress, paymentMethod, cartItems} = cart

    cart.itemsPrice = cartItems.reduce((acc, item) => acc + item.price*item.qty, 0).toFixed(2)
    cart.shippingPrice = (cart.itemsPrice>100 ? 0 : 10).toFixed(2)
    cart.taxPrice = Number(0.082 * cart.itemsPrice).toFixed(2)
    cart.totalPrice = (Number(cart.itemsPrice)+Number(cart.shippingPrice)+Number(cart.taxPrice)).toFixed(2)

    const dispatch = useDispatch()

    if (!paymentMethod) {
        history.push('/payment')
    }

    useEffect(() => {
        if(success){
            history.push(`/order/${order._id}`)
            dispatch({type: ORDER_CREATE_RESET})
        }
    }, [success, history, dispatch, order])

    const placeOrder = () => {
        dispatch(createOrder({
            orderItems: cartItems,
            shippingAddress: shippingAddress,
            paymentMethod: paymentMethod,
            itemsPrice: cart.itemsPrice,
            shippingPrice: cart.shippingPrice,
            taxPrice: cart.taxPrice,
            totalPrice: cart.totalPrice,
        }))
    }

    return (
        <div>
            <CheckoutSteps step1 step2 step3 step4/>
            <Row>
                <Col md={8}>
                    <ListGroup variant='flush'>
                        <ListGroup.Item>
                            <h2>Shipping</h2>
                            <p>
                                <strong>Shipping: </strong>
                                {shippingAddress.address}, {shippingAddress.city},
                                {'  '}
                                {shippingAddress.postalCode},
                                {'  '}
                                {shippingAddress.country}
                            </p>
                        </ListGroup.Item>

                        <ListGroup.Item>
                            <h2>Payment Method</h2>
                            <p>
                                <strong>Method: </strong>
                                {paymentMethod}
                            </p>
                        </ListGroup.Item>

                        <ListGroup.Item>
                            <h2>Order Items</h2>
                            {cartItems.length === 0 ? <Message variant='info'>
                                Your cart is empty
                            </Message> : (
                                <ListGroup variant='flush'>
                                    {cartItems.map((item, index) => (
                                        <ListGroup.Item key={index}>
                                            <Row>
                                                <Col md={1}>
                                                    <Image src={item.image} alt={item.name} fluid rounded />
                                                </Col>
                                                <Col>
                                                    <Link to={`/product/${item.product}`}>{item.name}</Link>
                                                </Col>
                                                <Col md={4}>
                                                    {item.qty} X ${item.price} = ${(item.qty * item.price).toFixed(2)}
                                                </Col>
                                            </Row>
                                        </ListGroup.Item>
                                    ))}
                                </ListGroup>
                            )}
                        </ListGroup.Item>
                    </ListGroup>
                </Col>

                <Col md={4}>
                    <Card>
                        <ListGroup variant='flush'>
                            <ListGroup.Item>
                                <h2>Order Summary</h2>
                            </ListGroup.Item>

                            <ListGroup.Item>
                                <Row>
                                    <Col>Items:</Col>
                                    <Col>${cart.itemsPrice}</Col>
                                </Row>
                            </ListGroup.Item>

                            <ListGroup.Item>
                                <Row>
                                    <Col>Shipping:</Col>
                                    <Col>${cart.shippingPrice}</Col>
                                </Row>
                            </ListGroup.Item>

                            <ListGroup.Item>
                                <Row>
                                    <Col>Tax:</Col>
                                    <Col>${cart.taxPrice}</Col>
                                </Row>
                            </ListGroup.Item>

                            <ListGroup.Item>
                                <Row>
                                    <Col>Total:</Col>
                                    <Col>${cart.totalPrice}</Col>
                                </Row>
                            </ListGroup.Item>

                            <ListGroup.Item>
                                {error && <Message variant='danger'>{error}</Message>}
                            </ListGroup.Item>

                            <ListGroup.Item>
                                <Button 
                                    type='button' 
                                    className='btn-block' 
                                    disabled={cartItems === 0}
                                    onClick={placeOrder}
                                >
                                    Place Order
                                </Button>
                            </ListGroup.Item>
                        </ListGroup>
                    </Card>
                                
                </Col>
            </Row>
        </div>
    )
}

export default PlaceOrderScreen;
