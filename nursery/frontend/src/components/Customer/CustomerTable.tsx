import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import axiosInstance from "../../api/axiosInstance";
import { Customer } from "../../types";
import PaginationControls from "../Common/PaginationControls"

interface CustomerTableProps {
  entities: Customer[];
  onSelectedIdsChanged: (selectedIds: number[]) => void;
}

const CustomerTable: React.FC<CustomerTableProps> = ({ entities, onSelectedIdsChanged }) => {
  const [selectedIds, setSelectedIds] = useState<number[]>([]);

  useEffect(() => {
      onSelectedIdsChanged(selectedIds)
  }, [selectedIds]);

  const toggleSelectRow = (id: number) => {
    setSelectedIds((prev) =>
      prev.includes(id) ? prev.filter((x) => x !== id) : [...prev, id]
    );
  };

  const allVisibleIds = entities.map((c) => c.id);
  const areAllSelected = allVisibleIds.every(id => selectedIds.includes(id));

  const toggleSelectAll = () => {
    if (areAllSelected) {
      setSelectedIds(prev => prev.filter(id => !allVisibleIds.includes(id)));
    } else {
      setSelectedIds(prev => [...new Set([...prev, ...allVisibleIds])]);
    }
  };

  return (
    <>
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
          {entities.map((c) => (
            <tr key={c.id}>
              <td>
                <input
                  type="checkbox"
                  checked={selectedIds.includes(c.id)}
                  onChange={() => toggleSelectRow(c.id)}
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
    </>
  );
};

export default CustomerTable;
