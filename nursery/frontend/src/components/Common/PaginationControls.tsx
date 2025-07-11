import React from "react";

interface PaginationInfo {
  page_num: number;
  total_pages: number;
}

interface PaginationControlsProps {
  pagination: PaginationInfo;
  onPrev: () => void;
  onNext: () => void;
}

const PaginationControls: React.FC<PaginationControlsProps> = ({
  pagination,
  onPrev,
  onNext,
}) => {
  return (
    <div style={{ marginTop: "1em" }}>
      <button onClick={onPrev} disabled={pagination.page_num <= 1}>← Prev</button>
      <span style={{ margin: "0 1em" }}>
        Page {pagination.page_num} of {pagination.total_pages}
      </span>
      <button onClick={onNext} disabled={pagination.page_num >= pagination.total_pages}>Next →</button>
    </div>
  );
};

export default PaginationControls;
