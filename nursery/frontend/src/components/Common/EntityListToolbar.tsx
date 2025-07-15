import React from "react";
import { useNavigate } from "react-router-dom";

interface ToolbarButton {
  caption: string;
  onClick: () => void;
  disabled?: boolean;
}

interface EntityListToolbarProps {
  newRowCaption: string;
  newRowRoute: string;
  numSelected: number;
  buttons: ToolbarButton[];
}

const EntityListToolbar: React.FC<EntityListToolbarProps> = ({
  newRowCaption,
  newRowRoute,
  numSelected,
  buttons
}) => {
  const navigate = useNavigate();

  return (
    <div className="ui-block">
      <button onClick={() => navigate(newRowRoute)}>{newRowCaption}</button>

      <span style={{margin: "0 0 0 1.5em", color: (numSelected ? "" : "#aaa") }}>
        {numSelected} selected
      </span>

      {buttons.map((button, idx) => (
        <button key={idx} onClick={button.onClick} disabled={button.disabled}
          style={{margin: "0 0 0 .75em" }}>
          {button.caption}
        </button>
      ))}

    </div>
  );
};

export default EntityListToolbar;
