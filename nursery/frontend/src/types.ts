

export interface Customer {
  id: number;
  first_name: string;
  last_name: string;
  email: string;
  address: string;
}

export interface OrderLine {
  sku: string;
  description: string;
  qty: number;
  price: number;
  ext_price: number;
}

export interface Order {
  id: number;
  customer_id: number;
  created_at: string;
  order_lines: OrderLine[];
  status: string;
}

