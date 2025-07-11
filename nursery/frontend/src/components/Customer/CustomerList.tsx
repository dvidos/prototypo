import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import CustomerFilters, { CustomerFilterValues } from "./CustomerFilters";
import CustomerTable from "./CustomerTable";

const CustomerList: React.FC = () => {
  const navigate = useNavigate();
  const [filters, setFilters] = useState<CustomerFilterValues>({
    firstName: "",
    email: "",
    address: "",
  });
  const [page, setPage] = useState(1);

  return (
    <div>
      <h2>Customers</h2>
      <button onClick={() => navigate("/customers/new")}>Add Customer</button>

      <CustomerFilters filters={filters} onChange={setFilters} />
      <CustomerTable filters={filters} page={page} onPageChange={setPage} />
    </div>
  );
};

export default CustomerList;
