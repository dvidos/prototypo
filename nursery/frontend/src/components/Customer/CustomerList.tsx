import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import axiosInstance from "../../api/axiosInstance";
import CustomerFilters, { CustomerFilterValues } from "./CustomerFilters";
import CustomerTable from "./CustomerTable";
import EntityListToolbar from "../Common/EntityListToolbar";


const CustomerList: React.FC = () => {
  const navigate = useNavigate();
  const [filters, setFilters] = useState<CustomerFilterValues>({
    firstName: "",
    email: "",
    address: "",
  });
  const [selectedIds, setSelectedIds] = useState<number[]>([]);
  const [page, setPage] = useState(1);

  const fetchRows = async () => {
    try {
      axiosInstance
        .get("/customers", {
          params: {
            page_num: page,
            first_name__icontains: filters.firstName || undefined,
            email__icontains: filters.email || undefined,
            address__icontains: filters.address || undefined,
          },
        })
        .then((res) => {
          // res.data has pagination (page_size, page_num, total_rows, total_pages)
          // and results, an array of rows
          // setCustomers(res.data.results);
          // setPagination(res.data.pagination);
          setPage(res.data.pagination.page_num);
        });
    } catch {
      alert("Failed fetching data");
    }
  };

  const handleBulkDelete = async () => {
    const confirmed = window.confirm(`Delete ${selectedIds.length} selected customers?`);
    if (!confirmed) return;

    try {
      await axiosInstance.post("/customers/bulk/delete", { ids: selectedIds });
      setSelectedIds([]);
      fetchRows(); // Refetch after delete
    } catch {
      alert("Bulk delete failed");
    }
  };

  return (
    <div>
      <h2>Customers</h2>

      <CustomerFilters filters={filters} onChange={setFilters} />
      <EntityListToolbar
        newRowCaption="New"
        newRowRoute="/customers/new"
        numSelected={selectedIds.length}
        buttons={[
            {"caption": "Bulk Delete", "onClick":handleBulkDelete, "disabled": selectedIds.length == 0},
            {"caption": "Alert", "onClick":()=>{window.alert("Alert!")}, "disabled": selectedIds.length == 0},
        ]}
      />
      <CustomerTable
        filters={filters}
        page={page}
        onPageChange={setPage}
        onSelectedIdsChanged={(ids) => setSelectedIds(ids)}
      />
    </div>
  );
};

export default CustomerList;
