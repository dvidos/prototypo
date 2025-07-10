import React, { useState, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import axiosInstance from "../../api/axiosInstance";
import { Order } from "../../types";


interface PaginationInfo {
  page_num: number;
  page_size: number;
  total_rows: number;
  total_pages: number;
}

const OrderList: React.FC = () => {
  const [orders, setOrders] = useState<Order[]>([]);
  const [pagination, setPagination] = useState<PaginationInfo | null>(null);
  const [page, setPage] = useState(1);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [deletingId, setDeletingId] = useState<number | null>(null);
  const navigate = useNavigate();

  const fetchOrders = (pageNum: number) => {
    setLoading(true);
    axiosInstance
      .get("/orders", { params: { page_num: pageNum } })
      .then((res) => {
        setOrders(res.data.results);
        setPagination(res.data.pagination);
        setLoading(false);
      })
      .catch(() => {
        setError("Failed to load orders");
        setLoading(false);
      });
  };

  useEffect(() => {
    fetchOrders(page)
  }, [page]);

  const handlePrev = () => {
    if (pagination && page > 1) setPage(page - 1);
  };

  const handleNext = () => {
    if (pagination && page < pagination.total_pages) setPage(page + 1);
  };

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
      <button onClick={() => navigate("/orders/new")}>Add Order</button>
      <table border={1} cellPadding={6} style={{ marginTop: 10 }}>
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
                <button onClick={() => navigate(`/orders/${order.id}/edit`)}>Edit</button>
                {" "}
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

      {pagination && (
        <div style={{ marginTop: "1em" }}>
          <button onClick={handlePrev} disabled={page <= 1}>← Prev</button>
          <span style={{ margin: "0 1em" }}>
            Page {pagination.page_num} of {pagination.total_pages}
          </span>
          <button onClick={handleNext} disabled={page >= pagination.total_pages}>Next →</button>
        </div>
      )}
    </div>
  );
};

export default OrderList;
