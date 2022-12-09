import json


def test_add_item_1_json():
    result = {
        'items': {
            'black-coffee': {
                'type': {
                    '50 ml': {
                        'quantity': 5,
                        'price': '50.00',
                        'total_price': '250.00'
                    }
                },
                'img': 'None',
                'name': 'Black Coffee'
            }
        }
    }
    return result


def test_add_item_2_json():
    result = {
        'items': {
            'black-coffee': {
                'type': {
                    '50 ml': {
                        'quantity': 15,
                        'price': '50.00',
                        'total_price': '750.00'
                    }
                },
                'img': 'None',
                'name': 'Black Coffee'
            }
        }
    }
    return result


def test_add_item_3_json():
    result = {
        'items': {
            'black-coffee': {
                'type': {
                    '50 ml': {
                        'quantity': 15,
                        'price': '50.00',
                        'total_price': '750.00'
                    },
                    '100 ml': {
                        'quantity': 5,
                        'price': '50.00',
                        'total_price': '250.00'}
                },
                'img': 'None',
                'name': 'Black Coffee'
            }
        }
    }
    return result


def test_add_item_4_json():
    result = {
        'items': {
            'black-coffee': {
                'type': {
                    '50 ml': {
                        'quantity': 15,
                        'price': '50.00',
                        'total_price': '750.00'
                    },
                    '100 ml': {
                        'quantity': 15,
                        'price': '50.00',
                        'total_price': '750.00'}
                },
                'img': 'None',
                'name': 'Black Coffee'
            }
        }
    }
    return result


def test_add_item_5_json():
    result = {
        'items': {
            'black-coffee': {
                'type': {
                    '50 ml': {
                        'quantity': 15,
                        'price': '50.00',
                        'total_price': '750.00'
                    },
                    '100 ml': {
                        'quantity': 15,
                        'price': '50.00',
                        'total_price': '750.00'}
                },
                'img': 'None',
                'name': 'Black Coffee'
            },
            'white-coffee': {
                'type': {
                    '50 ml': {
                        'quantity': 5,
                        'price': '50.00',
                        'total_price': '250.00'
                    }
                },
                'img': 'None',
                'name': 'White Coffee'}
        }
    }
    return result


def test_delete_item_1_json():
    result = {
        'items': {
            'black-coffee': {
                'type': {
                    '50 ml': {
                        'quantity': 5,
                        'price': '50.00',
                        'total_price': '250.00'
                    }
                },
                'img': 'None',
                'name': 'Black Coffee'
            },
            'white-coffee': {
                'type': {
                    '50 ml': {
                        'quantity': 5,
                        'price': '50.00',
                        'total_price': '250.00'
                    }
                },
                'img': 'None',
                'name': 'White Coffee'
            }
        }
    }
    return result


def test_delete_item_2_json():
    result = {
        'items': {
            'white-coffee': {
                'type': {
                    '50 ml': {
                        'quantity': 5,
                        'price': '50.00',
                        'total_price': '250.00'
                    }
                },
                'img': 'None',
                'name': 'White Coffee'
            }
        }
    }
    return result


def test_remove_item_1_json():
    result = {
        'items': {
            'black-coffee': {
                'type': {
                    '50 ml': {
                        'quantity': 1,
                        'price': '50.00',
                        'total_price': '50.00'
                    }
                },
                'img': 'None',
                'name': 'Black Coffee'
            },
            'white-coffee': {
                'type': {
                    '50 ml': {
                        'quantity': 1,
                        'price': '50.00',
                        'total_price': '50.00'
                    }
                },
                'img': 'None',
                'name': 'White Coffee'
            }
        }
    }
    return result


def test_remove_item_2_json():
    result = {
        'items': {
            'black-coffee': {
                'type': {
                    '50 ml': {
                        'quantity': 1,
                        'price': '50.00',
                        'total_price': '50.00'
                    }
                },
                'img': 'None',
                'name': 'Black Coffee'
            }
        }
    }
    return result
