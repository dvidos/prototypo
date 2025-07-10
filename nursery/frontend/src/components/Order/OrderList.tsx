import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import axiosInstance from "../../api/axiosInstance";
import { Order } from "../../types";


const OrderList: React.FC = () => {
  const [orders, setOrders] = useState<Order[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [deletingId, setDeletingId] = useState<number | null>(null);

  useEffect(() => {
    axiosInstance.get("/orders")
      .then((res) => {
        setOrders(res.data);
        setLoading(false);
      })
      .catch(() => {
        setError("Failed to fetch orders");
        setLoading(false);
      });
  }, []);

  const handleDelete = async (id: number) => {
    const confirmed = window.confirm("Are you sure you want to delete this order?");
    if (!confirmed) return;

    setDeletingId(id);
    try {
      await axiosInstance.delete(`/orders/${id}`);
      setOrders(orders.filter(order => order.id !== id));
    } catch {
      alert("Failed to delete order");
    } finally {
      setDeletingId(null);
    }
  };

  if (loading) return <p>Loading orders...</p>;
  if (error) return <p>{error}</p>;

  return (
    <div>
      <h2>Orders</h2>
      <Link to="/orders/new">➕ Add Order</Link>
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Customer ID</th>
            <th>Created At</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {orders.map(order => (
            <tr key={order.id}>
              <td>{order.id}</td>
              <td>{order.customer_id}</td>
              <td>{new Date(order.created_at).toLocaleString()}</td>
              <td>
                <Link to={`/orders/${order.id}/edit`}>Edit</Link>&nbsp;
                <button
                  onClick={() => handleDelete(order.id)}
                  disabled={deletingId === order.id}
                >
                  {deletingId === order.id ? "Deleting..." : "Delete"}
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default OrderList;
