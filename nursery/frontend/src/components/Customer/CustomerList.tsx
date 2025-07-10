import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import axios from "axios";


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

  useEffect(() => {
    axios
      .get<Customer[]>("http://localhost:8000/api/customers")
      .then((res) => {
        setCustomers(res.data);
        setLoading(false);
      })
      .catch(() => {
        setError("Failed to load customers");
        setLoading(false);
      });
  }, []);

  if (loading) return <p>Loading customers...</p>;
  if (error) return <p>{error}</p>;

  return (
    <div>
      <h2>Customers</h2>
      <ul>
        {customers.map((c: Customer) => (
          <li key={c.id}>
            {c.first_name} {c.last_name} — {c.email} — {c.address} -
            <Link to={`/customers/${c.id}/edit`}>Edit</Link>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default CustomerList;
