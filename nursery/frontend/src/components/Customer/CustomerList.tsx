import React, { useState, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import axiosInstance from "../../api/axiosInstance";
import { Customer } from "../../types";

interface PaginationInfo {
  page_num: number;
  page_size: number;
  total_rows: number;
  total_pages: number;
}

const CustomerList: React.FC = () => {
  const [customers, setCustomers] = useState<Customer[]>([]);
  const [pagination, setPagination] = useState<PaginationInfo | null>(null);
  const [page, setPage] = useState(1);
  const [firstNameFilter, setFirstNameFilter] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string>("");
  const [deletingId, setDeletingId] = useState<number | null>(null);
  const navigate = useNavigate();

  const fetchCustomers = (pageNum: number) => {
    setLoading(true);
    axiosInstance
      .get("/customers", { params: {
          page_num: pageNum,
          first_name__icontains: firstNameFilter || undefined
      } })
      .then((res) => {
        setCustomers(res.data.results);
        setPagination(res.data.pagination);
        setLoading(false);
      })
      .catch(() => {
        setError("Failed to load customers");
        setLoading(false);
      });
  };

  useEffect(() => {
    fetchCustomers(page);
  }, [page]);

  useEffect(() => {
    if (page !== 1) {
      setPage(1);
    } else {
      fetchCustomers(1);  // explicitly fetch if already on page 1
    }
  }, [firstNameFilter]);

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

  const handlePrev = () => {
    if (pagination && page > 1) setPage(page - 1);
  };

  const handleNext = () => {
    if (pagination && page < pagination.total_pages) setPage(page + 1);
  };

  if (loading) return <p>Loading customers...</p>;
  if (error) return <p>{error}</p>;

  return (
    <div>
      <h2>Customers</h2>

      <button onClick={() => navigate("/customers/new")}>Add Customer</button>

      <div style={{ marginBottom: 12, padding: 8, border: "1px solid #ccc", borderRadius: 4 }}>
        <strong>Filters</strong><br />
        <input
          type="text"
          placeholder="First name contains..."
          value={firstNameFilter}
          onChange={(e) => {
            setFirstNameFilter(e.target.value);
          }}
        />
      </div>

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

export default CustomerList;
