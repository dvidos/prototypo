import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";

interface TableColumn<T> {
    caption: string;
    extractData: (entity: T) => string | number | React.ReactNode;
}

interface TableProps<T> {
  entities: T[];
  idExtraction: (entity: T) => number;
  columns: TableColumn<T>[];
  onSelectedIdsChanged: (selectedIds: number[]) => void;
}

function renderHeadersCell<T>(column: TableColumn<T>) {
    return <th>{column.caption}</th>;
}

function renderHeadersRow<T>(columns: TableColumn<T>[]) {
    return columns.map((col) => renderHeadersCell(col));
}

function renderEntityCell<T>(entity: T, column: TableColumn<T>) {
    return <td>{column.extractData(entity)}</td>;
}

function renderEntityRow<T>(entity: T, id: number, columns: TableColumn<T>[]) {
    return columns.map((col) => renderEntityCell(entity, col));
}

function EntityListTable<T>({
    entities, idExtraction, columns, onSelectedIdsChanged
}: TableProps<T>) {

  const [selectedIds, setSelectedIds] = useState<number[]>([]);

  useEffect(() => {
      onSelectedIdsChanged(selectedIds)
  }, [selectedIds]);

  const toggleSelectRow = (id: number) => {
    setSelectedIds((prev) =>
      prev.includes(id) ? prev.filter((x) => x !== id) : [...prev, id]
    );
  };

  const allVisibleIds = entities.map((c) => idExtraction(c));
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
              {renderEntityRow(c, id, columns)}
            </tr>
            )}
          )}
        </tbody>
      </table>
    </>
  );
};

export default EntityListTable;
