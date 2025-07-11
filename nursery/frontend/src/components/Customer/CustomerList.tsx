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
  const [selectedIds, setSelectedIds] = useState<number[]>([]);
  const [pagination, setPagination] = useState<PaginationInfo | null>(null);
  const [page, setPage] = useState(1);
  const [firstNameFilter, setFirstNameFilter] = useState("");
  const [debouncedFirstNameFilter, setDebouncedFirstNameFilter] = useState(firstNameFilter);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string>("");
  const [deletingId, setDeletingId] = useState<number | null>(null);
  const navigate = useNavigate();

  const fetchCustomers = (pageNum: number, firstNameFilter: string) => {
    setLoading(true);
    axiosInstance
      .get("/customers", { params: {
          page_num: pageNum,
          first_name__icontains: firstNameFilter || undefined
      } })
      .then((res) => {
        setCustomers(res.data.results);
        setPagination(res.data.pagination);
        setSelectedIds([]);
        setLoading(false);
      })
      .catch(() => {
        setError("Failed to load customers");
        setLoading(false);
      });
  };

  useEffect(() => {
    fetchCustomers(page, debouncedFirstNameFilter);
  }, [page, debouncedFirstNameFilter]);

  useEffect(() => {
    setPage(1);
  }, [debouncedFirstNameFilter]);

  useEffect(() => {
    const timeoutId = setTimeout(() => {
      setDebouncedFirstNameFilter(firstNameFilter)
    }, 500); // debounce

    return () => clearTimeout(timeoutId);
  }, [firstNameFilter]);

  const toggleSelection = (id: number) => {
    setSelectedIds((prev) =>
      prev.includes(id) ? prev.filter((x) => x !== id) : [...prev, id]
    );
  };

  const allVisibleIds = customers.map((c) => c.id);
  const areAllSelected = allVisibleIds.every(id => selectedIds.includes(id));

  const toggleSelectAll = () => {
    if (areAllSelected) {
      // Unselect all visible
      setSelectedIds((prev) => prev.filter(id => !allVisibleIds.includes(id)));
    } else {
      // Select all visible
      setSelectedIds((prev) => [...new Set([...prev, ...allVisibleIds])]);
    }
  };

  const handleBulkDelete = async () => {
    const confirmed = window.confirm(`Delete ${selectedIds.length} selected customers?`);
    if (!confirmed) return;

    try {
      await axiosInstance.post("/customers/bulk/delete", { ids: selectedIds });
      setSelectedIds([]);
      fetchCustomers(page, debouncedFirstNameFilter)
    } catch {
      alert("Bulk delete failed");
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

      <div style={{ margin: "1em 0", background: "#e7e7e7", padding: 10 }}>
        <strong>{selectedIds.length} selected</strong>
        <button onClick={handleBulkDelete} disabled={selectedIds.length == 0} style={{ marginLeft: 12 }}>
          Bulk Delete
        </button>
      </div>

      <table border={1} cellPadding={6} style={{ marginTop: 10 }}>
        <thead>
          <tr>
            <th><input type="checkbox" checked={areAllSelected} onChange={toggleSelectAll} /></th>
            <th>Name</th>
            <th>Email</th>
            <th>Address</th>
          </tr>
        </thead>
        <tbody>
          {customers.map((c) => (
            <tr key={c.id}>
              <td>
                <input
                  type="checkbox"
                  checked={selectedIds.includes(c.id)}
                  onChange={(e) => {
                    if (e.target.checked) {
                      setSelectedIds([...selectedIds, c.id]);
                    } else {
                      setSelectedIds(selectedIds.filter ((id) => id !== c.id));
                    }
                  }}
                />
              </td>
              <td>
                <Link to={`/customers/${c.id}/edit`}>{c.first_name} {c.last_name}</Link>
              </td>
              <td>{c.email}</td>
              <td>{c.address}</td>
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
