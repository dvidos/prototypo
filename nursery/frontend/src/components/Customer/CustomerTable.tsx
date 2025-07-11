import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import axiosInstance from "../../api/axiosInstance";
import { Customer } from "../../types";
import PaginationControls from "../Common/PaginationControls"

interface PaginationInfo {
  page_num: number;
  page_size: number;
  total_rows: number;
  total_pages: number;
}

interface CustomerTableProps {
  filters: {
    firstName: string;
    email: string;
    address: string;
  };
  page: number;
  onPageChange: (page: number) => void;
}

const CustomerTable: React.FC<CustomerTableProps> = ({ filters, page, onPageChange }) => {
  const [customers, setCustomers] = useState<Customer[]>([]);
  const [pagination, setPagination] = useState<PaginationInfo | null>(null);
  const [selectedIds, setSelectedIds] = useState<number[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string>("");

  // Debounce filters
  const [debouncedFilters, setDebouncedFilters] = useState(filters);
  useEffect(() => {
    const timeoutId = setTimeout(() => {
      setDebouncedFilters(filters);
    }, 500);
    return () => clearTimeout(timeoutId);
  }, [filters]);

  useEffect(() => {
    // reset page to 1 if filters change
    onPageChange(1);
  }, [debouncedFilters]); // only once when filters stabilize

  useEffect(() => {
    setLoading(true);
    axiosInstance
      .get("/customers", {
        params: {
          page_num: page,
          first_name__icontains: debouncedFilters.firstName || undefined,
          email__icontains: debouncedFilters.email || undefined,
          address__icontains: debouncedFilters.address || undefined,
        },
      })
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
  }, [page, debouncedFilters]);

  const toggleSelection = (id: number) => {
    setSelectedIds((prev) =>
      prev.includes(id) ? prev.filter((x) => x !== id) : [...prev, id]
    );
  };

  const allVisibleIds = customers.map((c) => c.id);
  const areAllSelected = allVisibleIds.every(id => selectedIds.includes(id));

  const toggleSelectAll = () => {
    if (areAllSelected) {
      setSelectedIds(prev => prev.filter(id => !allVisibleIds.includes(id)));
    } else {
      setSelectedIds(prev => [...new Set([...prev, ...allVisibleIds])]);
    }
  };

  const handleBulkDelete = async () => {
    const confirmed = window.confirm(`Delete ${selectedIds.length} selected customers?`);
    if (!confirmed) return;

    try {
      await axiosInstance.post("/customers/bulk/delete", { ids: selectedIds });
      setSelectedIds([]);
      // Refetch after delete
      axiosInstance
        .get("/customers", {
          params: {
            page_num: page,
            first_name__icontains: debouncedFilters.firstName || undefined,
            email__icontains: debouncedFilters.email || undefined,
            address__icontains: debouncedFilters.address || undefined,
          },
        })
        .then((res) => {
          setCustomers(res.data.results);
          setPagination(res.data.pagination);
        });
    } catch {
      alert("Bulk delete failed");
    }
  };

  const handlePrev = () => {
    if (pagination && page > 1) onPageChange(page - 1);
  };

  const handleNext = () => {
    if (pagination && page < pagination.total_pages) onPageChange(page + 1);
  };

  if (loading) return <p>Loading customers...</p>;
  if (error) return <p>{error}</p>;

  return (
    <>
      <div style={{ margin: "1em 0", background: "#e7e7e7", padding: 10 }}>
        <strong>{selectedIds.length} selected</strong>
        <button onClick={handleBulkDelete} disabled={selectedIds.length === 0} style={{ marginLeft: 12 }}>
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
                  onChange={() => toggleSelection(c.id)}
                />
              </td>
              <td>
                <Link to={`/customers/${c.id}/edit`}>
                  {c.first_name} {c.last_name}
                </Link>
              </td>
              <td>{c.email}</td>
              <td>{c.address}</td>
            </tr>
          ))}
        </tbody>
      </table>

      {pagination && (
        <PaginationControls
          pagination={pagination}
          onPrev={handlePrev}
          onNext={handleNext}
        />
      )}
    </>
  );
};

export default CustomerTable;
