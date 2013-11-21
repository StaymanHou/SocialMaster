module ApplicationHelper
	def to_bool(s)
		return true if s == true || s =~ (/(true|t|yes|y|1)$/i)
		return false if s == false || s.empty? || s =~ (/(false|f|no|n|0)$/i)
		raise ArgumentError.new("invalid value for Boolean: \"#{s}\"")
	end
end
