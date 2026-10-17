import React from 'react';

const Button = ({ children, onClick, disabled, className, ...props }) => {
  return (
    <button 
      onClick={onClick}
      disabled={disabled}
      className={`px-4 py-2 rounded-md font-medium transition-colors ${className || ''} ${disabled ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'}`}
      {...props}
    >
      {children}
    </button>
  );
};

Button.defaultProps = {
  onClick: undefined,
  disabled: false,
};

export default Button;