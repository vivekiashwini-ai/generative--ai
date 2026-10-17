import React from 'react';

const Input = ({ type, placeholder, value, onChange, ...props }) => {
  return (
    <input 
      type={type}
      placeholder={placeholder}
      value={value}
      onChange={onChange}
      className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm dark:bg-gray-700 dark:text-white"
      {...props}
    />
  );
};

Input.defaultProps = {
  type: 'text',
};

export default Input;