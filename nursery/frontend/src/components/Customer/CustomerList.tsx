import React, { useState, useEffect } from "react";
import { useNavigate, Link } from "react-router-dom";
import axiosInstance from "../../api/axiosInstance";
import EntityListToolbar from "../Common/EntityListToolbar";
import EntityListTable from "../Common/EntityListTable";
import FiltersPanel, { FilterType } from "../Common/FiltersPanel";
import PaginationControls from "../Common/PaginationControls";
import { Customer } from "../../types";

interface PaginationInfo {  // as returned in the GET endpoint response
  page_num: number;
  page_size: number;
  total_rows: number;
  total_pages: number;
}

const CustomerList: React.FC = () => {
  const navigate = useNavigate();
  const [desiredPage, setDesiredPage] = useState(1);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string>("");
  const [filters, setFilters] = useState<Record<string, string | boolean | string[] | null>>({
    firstName: "",
    email: "",
    address: "",
  });
  const [pagination, setPagination] = useState<PaginationInfo>({page_num: 0, page_size: 1, total_rows: 0, total_pages: 0});
  const [selectedIds, setSelectedIds] = useState<number[]>([]);
  const [customers, setCustomers] = useState<Customer[]>([]);

  useEffect(() => {
      setDesiredPage(1);
  }, []);

  useEffect(() => {
      console.log("Desired page changed:", desiredPage);
      if (pagination.page_num != desiredPage)
        fetchRows();
  }, [desiredPage]);

  useEffect(() => {
    const timeout = setTimeout(() => {
      console.log("Debounced filter change:", filters);
      fetchRows();
    }, 300); // delay in ms

    return () => clearTimeout(timeout); // cleanup if filters change again within delay
  }, [filters]);

  const fetchRows = async () => {
    console.log("Fetching rows for page", desiredPage, "with filters", filters);
    try {
      setLoading(true);
      axiosInstance
        .get("/customers/", {
          params: {
            page_num: desiredPage,
            first_name__icontains: filters.firstName || undefined,
            email__icontains: filters.email || undefined,
            address__icontains: filters.address || undefined,
          },
        })
        .then((res) => {
          // res.data has pagination (page_size, page_num, total_rows, total_pages)
          // and results, an array of rows
          setCustomers(res.data.results);
          setPagination(res.data.pagination);
          if (res.data.pagination.page_num !== desiredPage)
            setDesiredPage(res.data.pagination.page_num);
          setLoading(false);
        });
    } catch {
      alert("Failed fetching data");
      setLoading(false);
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

  const handlePrevPage = () => {
    if (pagination && pagination.page_num > 1)
        setDesiredPage(pagination.page_num - 1);
  };

  const handleNextPage = () => {
    if (pagination && pagination.page_num < pagination.total_pages)
        setDesiredPage(pagination.page_num + 1);
  };

  if (loading) return <p>Loading customers...</p>;
  if (error) return <p>{error}</p>;

  return (
    <div>
      <h2>Customers</h2>

      <FiltersPanel
        attributes={[
          { name: "firstName", caption: "First name", type: FilterType.Text },
          { name: "email", caption: "Email", type: FilterType.Text, },
          { name: "subscribed", caption: "Subscribed", type: FilterType.Checkbox, },
          { name: "country", caption: "Country", type: FilterType.Dropdown, options: [ { value: "us", caption: "USA" }, { value: "gr", caption: "Greece" } ] }
        ]}
        values={filters}
        onValuesChanged={setFilters}
      />

      <EntityListToolbar
        newRowCaption="New"
        newRowRoute="/customers/new"
        numSelected={selectedIds.length}
        buttons={[
            {"caption": "Bulk Delete", "onClick":handleBulkDelete, "disabled": selectedIds.length == 0},
            {"caption": "Alert", "onClick":()=>{window.alert("Alert!")}, "disabled": selectedIds.length == 0},
        ]}
      />

      <EntityListTable
        entities={customers}
        idExtraction={(customer) => customer.id}
        columns={[
          {caption: "Full Name", extractData: (c: Customer) => (
              <Link to={`/customers/${c.id}/edit`}>
                {c.first_name} {c.last_name}
              </Link>
          )},
          {caption: "Address", extractData: (c: Customer) => c.address },
          {caption: "Email", extractData: (c: Customer) => c.email },
          {caption: "Last Name", extractData: (c) => c.last_name }
        ]}
        onSelectedIdsChanged={(ids) => setSelectedIds(ids)}
      />

      <PaginationControls
        pageNum={pagination.page_num}
        totalPages={pagination.total_pages}
        onPrev={handlePrevPage}
        onNext={handleNextPage}
      />

    </div>
  );
};

export default CustomerList;
