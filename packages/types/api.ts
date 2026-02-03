/**
 * Code-Sentinel API Type Definitions
 * 
 * This file contains TypeScript type definitions that mirror the Python Pydantic models
 * used in the FastAPI backend. These types ensure type safety and consistency between
 * the frontend and backend.
 */

/**
 * Severity level for code smells
 * 
 * Represents the severity of a detected code quality issue:
 * - "low": Minor issues that don't significantly impact code quality
 * - "medium": Moderate issues that should be addressed
 * - "high": Critical issues that require immediate attention
 */
export type Severity = "low" | "medium" | "high";

/**
 * Code Review Request
 * 
 * Represents a request to review code for quality issues.
 * 
 * @property code - The code text to be reviewed
 *   - Must not be empty (min length: 1 character)
 *   - Maximum length: 100,000 characters
 *   - Required field
 * 
 * @property language - Programming language identifier
 *   - Default value: "python"
 *   - Examples: "python", "javascript", "typescript", "java", "go"
 *   - Optional field
 */
export interface CodeReviewRequest {
  /**
   * The code text to be reviewed
   * 
   * Constraints:
   * - Required field
   * - Must not be empty string
   * - Maximum length: 100,000 characters
   */
  code: string;

  /**
   * Programming language identifier
   * 
   * Constraints:
   * - Optional field
   * - Default value: "python" (applied by backend)
   * 
   * Examples: "python", "javascript", "typescript", "java", "go", "rust"
   */
  language?: string;
}

/**
 * Code Smell
 * 
 * Represents a single detected code quality issue (code smell).
 * Each code smell includes information about the type of issue, its severity,
 * location, description, and suggestions for fixing it.
 * 
 * @property type - The type/category of the code smell
 *   - Minimum length: 3 characters
 *   - Examples: "Long Method", "Magic Number", "Duplicate Code"
 *   - Required field
 * 
 * @property severity - The severity level of the issue
 *   - Must be one of: "low", "medium", "high"
 *   - Required field
 * 
 * @property line - The line number where the issue occurs
 *   - Must be a positive integer (> 0)
 *   - Required field
 * 
 * @property message - A description of the problem
 *   - Minimum length: 5 characters
 *   - Required field
 * 
 * @property suggestion - Guidance on how to fix the issue
 *   - Minimum length: 10 characters
 *   - Required field
 */
export interface CodeSmell {
  /**
   * The type/category of the code smell
   * 
   * Constraints:
   * - Required field
   * - Minimum length: 3 characters
   * 
   * Examples: "Long Method", "Magic Number", "Duplicate Code", "God Class"
   */
  type: string;

  /**
   * The severity level of the issue
   * 
   * Constraints:
   * - Required field
   * - Must be one of: "low", "medium", "high"
   * 
   * Severity meanings:
   * - "low": Minor issues that don't significantly impact code quality
   * - "medium": Moderate issues that should be addressed
   * - "high": Critical issues that require immediate attention
   */
  severity: Severity;

  /**
   * The line number where the issue occurs
   * 
   * Constraints:
   * - Required field
   * - Must be a positive integer (> 0)
   * 
   * Note: Line numbers are 1-indexed (first line is line 1)
   */
  line: number;

  /**
   * A description of the problem
   * 
   * Constraints:
   * - Required field
   * - Minimum length: 5 characters
   * 
   * Should clearly explain what the issue is and why it's problematic
   */
  message: string;

  /**
   * Guidance on how to fix the issue
   * 
   * Constraints:
   * - Required field
   * - Minimum length: 10 characters
   * 
   * Should provide actionable advice on how to resolve the code smell
   */
  suggestion: string;
}

/**
 * Code Review Response
 * 
 * Represents the response from a code review request.
 * Contains the processing status, a list of detected code smells,
 * and a summary of the analysis.
 * 
 * @property status - The processing status
 *   - Current implementation always returns "success"
 *   - Required field
 * 
 * @property smells - List of detected code quality issues
 *   - Minimum length: 1 element
 *   - Current implementation returns exactly 3 smells (mock data)
 *   - Required field
 * 
 * @property summary - A summary of the analysis results
 *   - Minimum length: 10 characters
 *   - Format: "分析了 {字符数} 个字符的 {语言} 代码，发现 {数量} 个潜在问题"
 *   - Required field
 */
export interface CodeReviewResponse {
  /**
   * The processing status
   * 
   * Constraints:
   * - Required field
   * 
   * Current implementation:
   * - Always returns "success" for valid requests
   * - Future implementations may include "error" or "partial" statuses
   */
  status: string;

  /**
   * List of detected code quality issues
   * 
   * Constraints:
   * - Required field
   * - Minimum length: 1 element
   * 
   * Current implementation:
   * - Returns exactly 3 mock code smells:
   *   1. Long Method (severity: "medium", line: 10)
   *   2. Magic Number (severity: "low", line: 15)
   *   3. Duplicate Code (severity: "high", line: 25)
   */
  smells: CodeSmell[];

  /**
   * A summary of the analysis results
   * 
   * Constraints:
   * - Required field
   * - Minimum length: 10 characters
   * 
   * Format:
   * - "分析了 {字符数} 个字符的 {语言} 代码，发现 {数量} 个潜在问题"
   * - Example: "分析了 150 个字符的 python 代码，发现 3 个潜在问题"
   * 
   * The summary includes:
   * - Exact character count of the submitted code
   * - Programming language from the request
   * - Number of detected code smells
   */
  summary: string;
}

/**
 * Health Check Response
 * 
 * Response from the health check endpoint.
 * Used for monitoring API availability and container health checks.
 */
export interface HealthCheckResponse {
  /**
   * Health status of the API
   * 
   * Values:
   * - "healthy": API is running normally
   */
  status: string;
}

/**
 * Root Endpoint Response
 * 
 * Response from the root endpoint.
 * Used for basic API availability checks.
 */
export interface RootResponse {
  /**
   * API status message
   * 
   * Value: "Code-Sentinel API is running"
   */
  message: string;
}

/**
 * Validation Error Detail
 * 
 * Represents a single validation error returned by FastAPI
 * when request validation fails (HTTP 422).
 */
export interface ValidationErrorDetail {
  /**
   * Location of the error in the request
   * 
   * Example: ["body", "code"] indicates an error in the "code" field of the request body
   */
  loc: (string | number)[];

  /**
   * Human-readable error message
   * 
   * Example: "field required", "ensure this value has at least 1 characters"
   */
  msg: string;

  /**
   * Error type identifier
   * 
   * Example: "value_error.missing", "value_error.any_str.min_length"
   */
  type: string;
}

/**
 * Validation Error Response
 * 
 * Response structure returned by FastAPI when request validation fails.
 * HTTP Status Code: 422 Unprocessable Entity
 */
export interface ValidationErrorResponse {
  /**
   * Array of validation error details
   * 
   * Each element describes a specific validation failure
   */
  detail: ValidationErrorDetail[];
}
