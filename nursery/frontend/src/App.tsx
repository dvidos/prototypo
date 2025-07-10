import React from "react";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";

import CustomerList from "./components/Customer/CustomerList";
import CustomerForm from "./components/Customer/CustomerForm";
import OrderList from "./components/Order/OrderList";
import OrderForm from "./components/Order/OrderForm";

const App: React.FC = () => {
  return (
    <Router>
      <nav style={{ marginBottom: 20 }}>
        <Link to="/customers">Customers</Link> |{" "}
        <Link to="/orders">Orders</Link>
      </nav>
      <Routes>
        <Route path="/customers" element={<CustomerList />} />
        <Route path="/customers/new" element={<CustomerForm />} />
        <Route path="/customers/:id/edit" element={<CustomerForm />} />
        <Route path="/orders" element={<OrderList />} />
        <Route path="/orders/new" element={<OrderForm />} />
        <Route path="/orders/:id/edit" element={<OrderForm />} />
        <Route path="*" element={<h2>Welcome to Nursery App</h2>} />
      </Routes>
    </Router>
  );
};

export default App;
