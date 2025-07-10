import React, { useState, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import axiosInstance from "../../api/axiosInstance";
import { Customer } from "../../types";

const CustomerList: React.FC = () => {
  const [customers, setCustomers] = useState<Customer[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string>("");
  const [deletingId, setDeletingId] = useState<number | null>(null);
  const navigate = useNavigate();

  useEffect(() => {
    axiosInstance
      .get<Customer[]>("/customers")
      .then((res) => {
        setCustomers(res.data);
        setLoading(false);
      })
      .catch(() => {
        setError("Failed to load customers");
        setLoading(false);
      });
  }, []);

  const handleDelete = async (id: number) => {
    const confirmed = window.confirm("Are you sure you want to delete this customer?");
    if (!confirmed) return;

    setDeletingId(id);
    try {
      await axiosInstance.delete(`/customers/${id}`);
      setCustomers(customers.filter((c) => c.id !== id));
    } catch {
      alert("Failed to delete customer");
    } finally {
      setDeletingId(null);
    }
  };

  if (loading) return <p>Loading customers...</p>;
  if (error) return <p>{error}</p>;

  return (
    <div>
      <h2>Customers</h2>
      <button onClick={() => navigate("/customers/new")}>Add Customer</button>
      <table border={1} cellPadding={6} style={{ marginTop: 10 }}>
        <thead>
          <tr>
            <th>Name</th>
            <th>Email</th>
            <th>Address</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {customers.map((c) => (
            <tr key={c.id}>
              <td>{c.first_name} {c.last_name}</td>
              <td>{c.email}</td>
              <td>{c.address}</td>
              <td>
                <button onClick={() => navigate(`/customers/${c.id}/edit`)}>Edit</button>
                {" "}
                <button
                  onClick={() => handleDelete(c.id)}
                  disabled={deletingId === c.id}
                >
                  {deletingId === c.id ? "Deleting..." : "Delete"}
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default CustomerList;
