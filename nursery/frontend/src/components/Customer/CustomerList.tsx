import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import axiosInstance from "../../api/axiosInstance";


interface Customer {
  id: number;
  first_name: string;
  last_name: string;
  email: string;
  address: string;
}

const CustomerList: React.FC = () => {
  const [customers, setCustomers] = useState<Customer[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string>("");
  const [deletingId, setDeletingId] = useState<number | null>(null);

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
    } catch (err) {
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
      <ul>
        {customers.map((c: Customer) => (
          <li key={c.id}>
            {c.first_name} {c.last_name} — {c.email} — {c.address} -
            {'\u00A0'}{/* non-breaking space */}
            <Link to={`/customers/${c.id}/edit`}>Edit</Link>
            {'\u00A0'}{/* non-breaking space */}
            <button
                onClick={() => handleDelete(c.id)}
                disabled={deletingId === c.id}
            >
              {deletingId === c.id ? "Deleting..." : "Delete"}
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default CustomerList;
