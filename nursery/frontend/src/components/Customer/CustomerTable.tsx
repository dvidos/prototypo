import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import axiosInstance from "../../api/axiosInstance";
import { Customer } from "../../types";
import PaginationControls from "../Common/PaginationControls"

interface TableColumn {
    caption: string;
    extractData: (entity: Customer) => string;
}

interface CustomerTableProps {
  entities: Customer[];
  idExtraction: (entity: Customer) => number;
  columns: TableColumn[];
  onSelectedIdsChanged: (selectedIds: number[]) => void;
}

function renderHeadersCell(column: TableColumn) {
    return <th>{column.caption}</th>;
}

function renderHeadersRow(columns: TableColumn[]) {
    return columns.map((col) => renderHeadersCell(col));
}

function renderEntityCell(entity: any, column: TableColumn) {
    return <td>{column.extractData(entity)}</td>;
}

function renderEntityRow(entity: any, columns: TableColumn[]): any[] {
    return columns.map((col) => renderEntityCell(entity, col));
}

const CustomerTable: React.FC<CustomerTableProps> = ({ entities, idExtraction, columns, onSelectedIdsChanged }) => {
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
            <th>ID</th>
            <th>Name</th>
            <th>Email</th>
            <th>Address</th>
            {renderHeadersRow(columns)}
          </tr>
        </thead>
        <tbody>
          {entities.map((c) => {
            const id=idExtraction(c);
            return (
            <tr key={id}>
              <td>
                <input
                  type="checkbox"
                  checked={selectedIds.includes(id)}
                  onChange={() => toggleSelectRow(id)}
                />
              </td>
              <td>{id}</td>
              <td>
                <Link to={`/customers/${id}/edit`}>
                  {c.first_name} {c.last_name}
                </Link>
              </td>
              <td>{c.email}</td>
              <td>{c.address}</td>
              {renderEntityRow(c, columns)}
            </tr>
            )}
          )}
        </tbody>
      </table>
    </>
  );
};

export default CustomerTable;
