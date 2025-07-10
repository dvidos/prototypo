import React, { useState, useEffect } from "react";
import axios from "axios";


interface OrderLine {
  sku: string;
  description: string;
  qty: number;
  price: number;
  ext_price: number;
}

interface Order {
  id: number;
  created_at: string; // or Date, parsed from ISO string
  customer_id: number;
  total: number;
  order_lines: OrderLine[];
  status: string;
}

const OrderList: React.FC = () => {
  const [orders, setOrders] = useState<Order[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string>("");

  useEffect(() => {
    axios
      .get<Order[]>("http://localhost:8000/api/orders")
      .then((res) => {
        setOrders(res.data);
        setLoading(false);
      })
      .catch(() => {
        setError("Failed to load orders");
        setLoading(false);
      });
  }, []);

  if (loading) return <p>Loading orders...</p>;
  if (error) return <p>{error}</p>;

  return (
    <div>
      <h2>Orders</h2>
      {orders.map((order: Order) => (
        <div key={order.id} style={{ border: "1px solid gray", marginBottom: 20, padding: 10 }}>
          <p>
            <strong>Order #{order.id}</strong> - Customer ID: {order.customer_id} - {new Date(order.created_at).toLocaleString()}<br />
            Status: {order.status} - Total: ${order.total.toFixed(2)}
          </p>
          <table style={{ width: "100%", borderCollapse: "collapse" }}>
            <thead>
              <tr>
                <th>SKU</th>
                <th>Description</th>
                <th>Qty</th>
                <th>Price</th>
                <th>Ext. Price</th>
              </tr>
            </thead>
            <tbody>
              {order.order_lines.map((line: OrderLine) => (
                <tr key={line.sku}>
                  <td>{line.sku}</td>
                  <td>{line.description}</td>
                  <td>{line.qty}</td>
                  <td>${line.price.toFixed(2)}</td>
                  <td>${line.ext_price.toFixed(2)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ))}
    </div>
  );
};

export default OrderList;
