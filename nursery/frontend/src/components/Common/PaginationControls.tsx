import React from "react";

interface PaginationControlsProps {
  pageNum: number;
  totalPages: number;
  onPrev: () => void;
  onNext: () => void;
}

const PaginationControls: React.FC<PaginationControlsProps> = ({
  pageNum,
  totalPages,
  onPrev,
  onNext,
}) => {
  return (
    <div className="ui-block">

      <button onClick={onPrev} disabled={pageNum <= 1}>← Prev</button>

      <span style={{ margin: "0 1em" }}>
        Page {pageNum} of {totalPages}
      </span>

      <button onClick={onNext} disabled={pageNum >= totalPages}>Next →</button>

    </div>
  );
};

export default PaginationControls;
